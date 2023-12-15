import os
# from cloudmesh.common.Printer import Printer
import pprint
import sys
from datetime import date
from datetime import datetime
from signal import signal, SIGINT

import matplotlib.pyplot as plt
import xmltodict
import yaml

from cloudmesh.common.Shell import Shell
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import readfile
from cloudmesh.common.util import banner

from tabulate import tabulate
from cloudmesh.common.util import csv_to_list

class Gpu:

    def __init__(self, sep="T"):
        self.sep =sep
        self.running = True
        try:
            self._smi = dict(self.smi(output="json"))['nvidia_smi_log']['gpu']
            if not isinstance(self._smi, list):
                self._smi = [self._smi]
        except KeyError:
            raise RuntimeError("nvidia-smi not installed.")
        self.gpus = 0

    def probe(self):
        banner("Cloudmesh GPU Probe", c="=")

        for label, command in [
             ("nvidia-smi", "nvidia-smi"),
        ]:
            try:
                banner(label)
                r = Shell.run(command)
                print (r)
            except:
                pass

        for label, command in [
            ("OS Info", "cat /etc/*release"),
        ]:
            try:
                banner(label)
                r = Shell.run(command)
                r = r.replace("=", ",")
                data = csv_to_list(r)
                print(tabulate(data, tablefmt='fancy_grid'))
            except:
                pass

        for label, command in [
            ("drivers list", "xxx ubuntu-drivers list")
        ]:
            try:
                banner(label)
                r = Shell.run(command)
                r = r.replace("kernel modules provided by", "")\
                    .replace("(","")\
                    .replace(")", "")\
                    .replace(" ", "")
                data = csv_to_list(r)
                print(tabulate(data,tablefmt='fancy_grid'))
            except:
                pass

        for label, command in [
             ("Nvidia Drivers","apt search nvidia-driver"),
        ]:
            try:
                banner(label)
                lines = Shell.run(command)\
                    .replace("\n  ", ";").splitlines()
                lines = [line.replace(" ", ";", 3) for line in lines]
                lines = "\n".join(lines).replace("\n\n", "\n")
                lines =  "\n".join(Shell.find_lines_from(lines, "nvidia"))

                data = csv_to_list(lines, sep=";")
                print(tabulate(data,tablefmt='fancy_grid'))
            except:
                pass



        return ""


    def fix_date_format(self, df, col):
        import pandas as pd
        # if We have T in it, we do not need to fix
        for i, row in df.iterrows():
            value = df.loc[i, col]
            if "T" not in value:
                new_date = df.loc[i, col].replace(":", " ", 1)
                df.loc[i, col] = new_date
        df[col] = pd.to_datetime(df[col])
        return df

    def read_eventlog(self, filename):
        import csv
        data = []
        header = None
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            data = list(reader)

        header = data[1]
        header[0] = "time"
        data = data[2:]
        return header, data


    def read_energy(self, filename=None):

        import pandas as pd
        import io

        location = Shell.map_filename(filename).path
        # 1: means removing hashes
        content = readfile(location).splitlines()[1:]
        # removing #
        content[0] = content[0][2:]
        # print(content[0:10])
        content = "\n".join(content)
        content = content.replace(', ', ',')
        df = pd.read_csv(io.StringIO(content), sep=',')

        df = self.fix_date_format(df, "time")
        df[["time"]] = df[["time"]].astype('datetime64[ns]')
        return df



    def export_figure(self, plt, x='Time/s', y='Energy/W',
                      filename="energy"):
        plt.xlabel(x)
        plt.ylabel(y)
        png = filename + ".png"
        pdf = filename + ".pdf"
        print ("Writing", png)
        plt.savefig(png, bbox_inches='tight', dpi=600)
        print ("Writing", pdf)
        plt.savefig(pdf, bbox_inches='tight')


    def graph(self, file, output, plot_type, histogram_frequency):
        import seaborn as sns
        import matplotlib.pyplot as plt
        from datetime import datetime
        import pandas as pd

        header, data = self.read_eventlog(file)
        time = []
        value = []
        for entry in data:
            t = entry[0]
            t = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%f')

            time.append(t)
            value.append(entry[7])
        x_label = "Time in s"
        y_label = "Power Draw in W"

        df = pd.DataFrame(
            {
                "time": time,
                "energy": value
            }
        )
        df['elapsed'] = df['time'] - pd.to_datetime(df['time'].values[0])

        df['elapsed_seconds'] = df.apply(
            lambda row: row.elapsed / pd.Timedelta(seconds=1), axis=1)
        df['energy'] = df.apply(lambda row: float(row.energy), axis=1)

        if plot_type == 'histogram':

            if histogram_frequency == 'percent':

                import numpy as np

                df["energy"].plot.hist(weights = np.ones_like(df.index) / len(df.index))
                plt.grid(True)

            else:
                df.hist(column='energy')
            plt.title('')
            x_label = 'Power Draw in W'
            y_label = 'Frequency'
        else:
            ax = sns.lineplot(x=f"elapsed_seconds", y="energy", data=df)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # taking out extension from file
        # first we determine if there is extension.
        if '.' in output:
            extension = str(os.path.splitext(output)[1])
            name_of_output = output
        # if there is none then we decide that the output is the extension.
        else:
            extension = '.' + output
            file = str(os.path.splitext(file)[0])
            name_of_output = file + extension

        # png = file + ".png"
        # pdf = file + ".pdf"


        if extension.lower() in [".jpg", ".png"]:
            # written_output = output
            plt.savefig(name_of_output, bbox_inches='tight', dpi=600)
        else:
            # written_output = 'pdf'
            plt.savefig(name_of_output, bbox_inches='tight')

        return f'Written to {name_of_output}'


    def exit_handler(self, signal_received, frame):
        """
        Kube manager has a build in Benchmark framework. In case you
        press CTRL-C, this handler assures that the benchmarks will be printed.

        :param signal_received:
        :type signal_received:
        :param frame:
        :type frame:
        :return:
        :rtype:
        """
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        self.running = False

    @property
    def count(self):
        if self.gpus == 0:
            try:
                self.gpus = int(Shell.run("nvidia-smi --list-gpus | wc -l").strip())
            except:
                self.gpus = 0
        return self.gpus

    def vendor(self):
        if os.name != "nt":
            try:
                r = Shell.run("lspci -vnn | grep VGA -A 12 | fgrep Subsystem:").strip()
                result = r.split("Subsystem:")[1].strip()
            except:
                result = None
        else:
            try:
                r = Shell.run("wmic path win32_VideoController get AdapterCompatibility").strip()
                result = [x.strip() for x in r.split("\r\r\n")[1:]]
            except Exception:
                results = None
        return result

    def processes(self):
        result = {}
        try:
            # We want to call this each time, as we want the current processes
            data = dict(self.smi(output="json"))["nvidia_smi_log"]['gpu']
            for i in range(self.count):
                information = data[i]["processes"]["process_info"]
                result[i] = information
        except Exception as e:
            print(e)
        return result

    def system(self):
        result = self._smi
        for gpu_instance in range(len(self._smi)):
            for attribute in [
                '@id',
                # 'product_name',
                # 'product_brand',
                # 'product_architecture',
                'display_mode',
                'display_active',
                'persistence_mode',
                'mig_mode',
                'mig_devices',
                'accounting_mode',
                'accounting_mode_buffer_size',
                'driver_model',
                'serial',
                'uuid',
                'minor_number',
                # 'vbios_version',
                'multigpu_board',
                'board_id',
                'gpu_part_number',
                'gpu_module_id',
                # 'inforom_version',
                'gpu_operation_mode',
                'gsp_firmware_version',
                'gpu_virtualization_mode',
                'ibmnpu',
                'pci',
                'fan_speed',
                'performance_state',
                'clocks_throttle_reasons',
                'fb_memory_usage',
                'bar1_memory_usage',
                'compute_mode',
                'utilization',
                'encoder_stats',
                'fbc_stats',
                'ecc_mode',
                'ecc_errors',
                'retired_pages',
                'remapped_rows',
                'temperature',
                'supported_gpu_target_temp',
                'power_readings',
                'clocks',
                'applications_clocks',
                'default_applications_clocks',
                'max_clocks',
                'max_customer_boost_clocks',
                'clock_policy',
                'voltage',
                'supported_clocks',
                'processes'
            ]:
                try:
                    del result[gpu_instance][attribute]
                    result[gpu_instance]["vendor"] = self.vendor()
                except KeyError:
                    pass
        return result

    def status(self):
        result = self._smi
        for gpu_instance in range(len(self._smi)):
            for attribute in [
                '@id',
                'product_name',
                'product_brand',
                'product_architecture',
                'display_mode',
                'display_active',
                'persistence_mode',
                'mig_mode',
                'mig_devices',
                'accounting_mode',
                'accounting_mode_buffer_size',
                'driver_model',
                'serial',
                'uuid',
                'minor_number',
                'vbios_version',
                'multigpu_board',
                'board_id',
                'gpu_part_number',
                'gpu_module_id',
                'inforom_version',
                'gpu_operation_mode',
                'gsp_firmware_version',
                'gpu_virtualization_mode',
                'ibmnpu',
                'pci',
                # 'fan_speed',
                'performance_state',
                'clocks_throttle_reasons',
                'fb_memory_usage',
                'bar1_memory_usage',
                'compute_mode',
                # 'utilization',
                'encoder_stats',
                'fbc_stats',
                'ecc_mode',
                'ecc_errors',
                'retired_pages',
                'remapped_rows',
                # 'temperature',
                # 'supported_gpu_target_temp',
                # 'power_readings',
                # 'clocks',
                'applications_clocks',
                'default_applications_clocks',
                'max_clocks',
                'max_customer_boost_clocks',
                'clock_policy',
                # 'voltage',
                'supported_clocks',
                'processes'
            ]:
                try:
                    del result[gpu_instance][attribute]
                except KeyError:
                    pass
        return result

    def smi(self, output=None, filename=None):
        # None = text
        # json
        # yaml
        try:
            if filename is None and output is None:
                result = Shell.run("nvidia-smi").replace("\r", "")
                return result

            if filename is not None:
                r = readfile(filename)
            else:
                r = Shell.run("nvidia-smi -q -x")
            if output == "xml":
                result = r
            elif output == "json":
                result = xmltodict.parse(r)

                if int(result["nvidia_smi_log"]["attached_gpus"]) == 1:
                    data = result["nvidia_smi_log"]["gpu"]
                    result["nvidia_smi_log"]["gpu"] = [data]

            elif output == "yaml":
                result = yaml.dump(xmltodict.parse(r))
        except Exception as e:
            print(e)
            result = None
        return result

    def watch(self, logfile=None, delay=1.0, repeated=None, dense=False, gpu=None):

        if repeated is None:
            repeated = -1
        else:
            repeated = int(repeated)

        try:
            delay = float(delay)
        except Exception as e:
            delay = 1.0

        signal(SIGINT, self.exit_handler)

        stream = sys.stdout
        if logfile is None:
            stream = sys.stdout
        else:
            stream = open(logfile, "w")

        print("# ####################################################################################")
        print("# time, ", end="")
        for i in range(self.count):
            print(
                f"{i} id, "
                f"{i} gpu_util %, "
                f"{i} memory_util %, "
                f"{i} encoder_util %, "
                f"{i} decoder_util %, "
                f"{i} gpu_temp C, "
                f"{i} power_draw W",
                end="")
        print()

        counter = repeated

        if gpu is not None:
            selected = [int(i) for i in gpu]
        else:
            selected = list(range(self.count))
        while self.running:
            try:
                if counter > 0:
                    counter = counter - 1
                    self.running = self.running and counter > 0
                today = date.today()
                now = datetime.now().time()  # time object
                data = self.smi(output="json")

                result = [f"{today}{self.sep}{now}"]

                for gpu in range(self.count):
                    if gpu in selected:
                        utilization = dotdict(data["nvidia_smi_log"]["gpu"][gpu]["utilization"])
                        temperature = dotdict(data["nvidia_smi_log"]["gpu"][gpu]["temperature"])
                        power = dotdict(data["nvidia_smi_log"]["gpu"][gpu]["power_readings"])
                        line = \
                            f"{gpu:>3}, " \
                            f"{utilization.gpu_util[:-2]: >3}, " \
                            f"{utilization.memory_util[:-2]: >3}, " \
                            f"{utilization.encoder_util[:-2]: >3}, " \
                            f"{utilization.decoder_util[:-2]: >3}, " \
                            f"{temperature.gpu_temp[:-2]: >5}, " \
                            f"{power.power_draw[:-2]: >8}"
                        result.append(line)

                result = ", ".join(result)
                if dense:
                    result = result.replace(" ", "")
                print(result, file=stream)

            except Exception as e:
                print(e)

    def __str__(self):
        return pprint.pformat(self._smi, indent=2)
