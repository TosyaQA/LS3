import time
import pytest
import yaml
from count_files_and_size import count_files_and_size
from execute_command import execute_command

@pytest.fixture
def update_stat_fixture(request):
    # Получаем текущее время
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # Читаем конфигурацию из файла config.yaml
    config_file = "config.yaml"
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    folderin = config.get('folderin')
    folderout = config.get('folderout')
    folderext = config.get('folderext')

    # Подсчитываем количество файлов и их размер для каждой папки
    num_files_in, file_size_in = count_files_and_size(folderin)
    num_files_out, file_size_out = count_files_and_size(folderout)
    num_files_ext, file_size_ext = count_files_and_size(folderext)

    # Читаем статистику загрузки процессора из файла /proc/loadavg
    with open("/proc/loadavg", "r") as f:
        cpu_load = f.read()

    # Дописываем строку в файл stat.txt
    stat_file = "stat.txt"
    with open(stat_file, "a") as f:
        f.write(f"{current_time} - Files In: {num_files_in}, Size In: {file_size_in}, Files Out: {num_files_out}, Size Out: {file_size_out}, Files Ext: {num_files_ext}, Size Ext: {file_size_ext}, CPU Load: {cpu_load}\n")

@pytest.mark.usefixtures("update_stat_fixture")
def test_list_files(command, expected_files):
    assert execute_command(command, '\n'.join(expected_files)) == True, f"Ошибка: файлы {expected_files} не найдены"

@pytest.mark.usefixtures("update_stat_fixture")
def test_extract_archive(command, expected_files):
    assert execute_command(command, '\n'.join(expected_files)) == True, f"Ошибка: файлы {expected_files} не удалось разархивировать"

test_extract_archive("unzip -j archive.zip", ["file1.txt", "file2.txt", "file3.txt"])

test_list_files("ls", ["file1.txt", "file2.txt", "file3.txt"])