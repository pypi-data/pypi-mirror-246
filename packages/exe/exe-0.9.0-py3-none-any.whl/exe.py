import argparse
import compileall
import glob
import os
import shutil
import sys
import zipfile

import ccompiler

main = '''
#define UNICODE
#define _UNICODE

#include <Windows.h>
#include <PowerSetting.h>
#include <Shlwapi.h>

struct PyObject;

typedef long long Py_ssize_t;

struct PyWideStringList {
    Py_ssize_t length;
    wchar_t ** items;
};

struct PyConfig {
    int _config_init;
    int isolated;
    int use_environment;
    int dev_mode;
    int install_signal_handlers;
    int use_hash_seed;
    unsigned long hash_seed;
    int faulthandler;
    int tracemalloc;
    int perf_profiling;
    int import_time;
    int code_debug_ranges;
    int show_ref_count;
    int dump_refs;
    wchar_t * dump_refs_file;
    int malloc_stats;
    wchar_t * filesystem_encoding;
    wchar_t * filesystem_errors;
    wchar_t * pycache_prefix;
    int parse_argv;
    PyWideStringList orig_argv;
    PyWideStringList argv;
    PyWideStringList xoptions;
    PyWideStringList warnoptions;
    int site_import;
    int bytes_warning;
    int warn_default_encoding;
    int inspect;
    int interactive;
    int optimization_level;
    int parser_debug;
    int write_bytecode;
    int verbose;
    int quiet;
    int user_site_directory;
    int configure_c_stdio;
    int buffered_stdio;
    wchar_t * stdio_encoding;
    wchar_t * stdio_errors;
    int legacy_windows_stdio;
    wchar_t * check_hash_pycs_mode;
    int use_frozen_modules;
    int safe_path;
    int int_max_str_digits;
    int pathconfig_warnings;
    wchar_t * program_name;
    wchar_t * pythonpath_env;
    wchar_t * home;
    wchar_t * platlibdir;
    int module_search_paths_set;
    PyWideStringList module_search_paths;
    wchar_t * stdlib_dir;
    wchar_t * executable;
    wchar_t * base_executable;
    wchar_t * prefix;
    wchar_t * base_prefix;
    wchar_t * exec_prefix;
    wchar_t * base_exec_prefix;
    int skip_source_first_line;
    wchar_t * run_command;
    wchar_t * run_module;
    wchar_t * run_filename;
    int _install_importlib;
    int _init_main;
    int _is_python_build;
};

struct PyStatus {
    int _type;
    const char *func;
    const char *err_msg;
    int exitcode;
};

void (* PyConfig_InitIsolatedConfig)(PyConfig * config);
PyStatus (* PyConfig_SetString)(PyConfig * config, wchar_t ** config_str, const wchar_t * str);
PyStatus (* PyWideStringList_Append)(PyWideStringList * list, const wchar_t * item);
PyStatus (* Py_InitializeFromConfig)(PyConfig * config);
PyObject * (* PyImport_ImportModule)(const char * name);
PyObject * (* PyObject_CallMethod)(PyObject * obj, const char * name, const char * format, ...);
PyObject * (* PyObject_Str)(PyObject *);
PyObject * (* PyUnicode_AsEncodedString)(PyObject * unicode, const char * encoding, const char * errors);
PyObject * (* PyUnicode_FromWideChar)(const wchar_t * w, Py_ssize_t size);
wchar_t * (* PyUnicode_AsWideCharString)(PyObject * unicode, Py_ssize_t * size);
PyObject * (* PyList_New)(Py_ssize_t size);
int (* PyList_SetItem)(PyObject *, Py_ssize_t, PyObject *);
PyObject * (* PyErr_GetRaisedException)();
void (* PyErr_DisplayException)(PyObject *);

wchar_t root_path[1024];
wchar_t python_dll[1024];
wchar_t python_path[1024];
wchar_t python_zip[1024];
PyConfig config = {};

extern "C" {
    _declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
    _declspec(dllexport) int AmdPowerXpressRequestHighPerformance = 0x00000001;
}

#ifdef NO_CONSOLE
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
#else
int main() {
#endif

    PowerSetActiveScheme(NULL, &GUID_MIN_POWER_SAVINGS);
    SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
    SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS);

    HMODULE hmodule = GetModuleHandle(NULL);

    GetModuleFileName(hmodule, root_path, 1024);
    PathRemoveFileSpec(root_path);
    SetCurrentDirectory(root_path);

    PathCombine(python_path, root_path, L"python");
    PathCombine(python_dll, python_path, L"python312.dll");
    PathCombine(python_zip, python_path, L"python312.zip");

    HMODULE python = LoadLibrary(python_dll);
    if (!python) {
        MessageBox(NULL, L"Cannot find python", L"Error", MB_ICONERROR);
    }

    *(void **)&PyConfig_InitIsolatedConfig = (void *)GetProcAddress(python, "PyConfig_InitIsolatedConfig");
    *(void **)&PyConfig_SetString = (void *)GetProcAddress(python, "PyConfig_SetString");
    *(void **)&PyWideStringList_Append = (void *)GetProcAddress(python, "PyWideStringList_Append");
    *(void **)&Py_InitializeFromConfig = (void *)GetProcAddress(python, "Py_InitializeFromConfig");
    *(void **)&PyImport_ImportModule = (void *)GetProcAddress(python, "PyImport_ImportModule");
    *(void **)&PyObject_CallMethod = (void *)GetProcAddress(python, "_PyObject_CallMethod_SizeT");
    *(void **)&PyObject_Str = (void *)GetProcAddress(python, "PyObject_Str");
    *(void **)&PyUnicode_AsEncodedString = (void *)GetProcAddress(python, "PyUnicode_AsEncodedString");
    *(void **)&PyUnicode_FromWideChar = (void *)GetProcAddress(python, "PyUnicode_FromWideChar");
    *(void **)&PyUnicode_AsWideCharString = (void *)GetProcAddress(python, "PyUnicode_AsWideCharString");
    *(void **)&PyList_New = (void *)GetProcAddress(python, "PyList_New");
    *(void **)&PyList_SetItem = (void *)GetProcAddress(python, "PyList_SetItem");
    *(void **)&PyErr_GetRaisedException = (void *)GetProcAddress(python, "PyErr_GetRaisedException");
    *(void **)&PyErr_DisplayException = (void *)GetProcAddress(python, "PyErr_DisplayException");

    PyConfig_InitIsolatedConfig(&config);
    config.write_bytecode = 0;
    config.module_search_paths_set = 1;
    PyWideStringList_Append(&config.module_search_paths, python_zip);
    PyWideStringList_Append(&config.module_search_paths, python_path);
    PyWideStringList_Append(&config.module_search_paths, root_path);
    PyConfig_SetString(&config, &config.home, root_path);
    Py_InitializeFromConfig(&config);

    PyObject * module = PyImport_ImportModule("{module}");
    if (!module) {
        PyObject * exc = PyErr_GetRaisedException();
        PyErr_DisplayException(exc);
        wchar_t * message = PyUnicode_AsWideCharString(PyObject_Str(exc), NULL);
        #ifdef NO_CONSOLE
        MessageBox(NULL, message, L"Error", MB_ICONERROR);
        #endif
        return 0;
    }

    int argc = 0;
    wchar_t ** argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    PyObject * args = PyList_New(argc);
    for (int i = 0; i < argc; ++i) {
        PyList_SetItem(args, i, PyUnicode_FromWideChar(argv[i], -1));
    }

    PyObject * res = PyObject_CallMethod(module, "main", "(O)", args);
    if (!res) {
        PyObject * exc = PyErr_GetRaisedException();
        PyErr_DisplayException(exc);
        wchar_t * message = PyUnicode_AsWideCharString(PyObject_Str(exc), NULL);
        #ifdef NO_CONSOLE
        MessageBox(NULL, message, L"Error", MB_ICONERROR);
        #endif
        return 0;
    }

    return 0;
}
'''

resource = '''
101 ICON "{icon}"
'''

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
init = subparsers.add_parser('init')
build = subparsers.add_parser('build')

init.set_defaults(command='init')

build.set_defaults(command='build')
build.add_argument('output', default='main.exe')
build.add_argument('module', default='main')
build.add_argument('--console', action='store_true', default=False)
build.add_argument('--icon', default=None)


def run_init(args):
    home = os.path.dirname(sys.executable)
    pydir = 'python'
    libdir = 'build/Lib'

    if os.path.isdir(pydir):
        shutil.rmtree(pydir)

    os.makedirs(pydir)

    files = [
        'DLLs/_asyncio.pyd',
        'DLLs/_bz2.pyd',
        'DLLs/_ctypes.pyd',
        'DLLs/_decimal.pyd',
        'DLLs/_elementtree.pyd',
        'DLLs/_hashlib.pyd',
        'DLLs/_lzma.pyd',
        'DLLs/_msi.pyd',
        'DLLs/_multiprocessing.pyd',
        'DLLs/_overlapped.pyd',
        'DLLs/_queue.pyd',
        'DLLs/_socket.pyd',
        'DLLs/_sqlite3.pyd',
        'DLLs/_ssl.pyd',
        'DLLs/_uuid.pyd',
        'DLLs/_wmi.pyd',
        'DLLs/_zoneinfo.pyd',
        'DLLs/libcrypto-3.dll',
        'DLLs/libffi-8.dll',
        'DLLs/libssl-3.dll',
        'DLLs/pyexpat.pyd',
        'DLLs/select.pyd',
        'DLLs/sqlite3.dll',
        'DLLs/unicodedata.pyd',
        'DLLs/winsound.pyd',
        'LICENSE.txt',
        'python3.dll',
        'python312.dll',
        'vcruntime140_1.dll',
        'vcruntime140.dll',
    ]

    for name in files:
        shutil.copy(os.path.join(home, name), os.path.join(pydir, os.path.basename(name)))

    if os.path.isdir(libdir):
        shutil.rmtree(libdir)

    ignore = [
        '__pycache__',
        'ensurepip',
        'idlelib',
        'site-packages',
        'test',
        'tkinter',
        'turtledemo',
        'venv',
        'turtle.py',
    ]

    shutil.copytree(os.path.join(home, 'Lib'), libdir, ignore=lambda src, names: ignore)

    compileall.compile_dir(libdir, stripdir=libdir, force=True, quiet=2, legacy=True, invalidation_mode=2, optimize=2)

    with zipfile.ZipFile('python/python312.zip', 'w', compression=zipfile.ZIP_DEFLATED) as pack:
        for name in glob.glob(os.path.join(libdir, '**/*.pyc'), recursive=True):
            pack.write(name, name[len(libdir):])


def run_build(args):
    os.makedirs('build', exist_ok=True)

    with open('build/main.cpp', 'w') as f:
        f.write(main.replace('{module}', args.module))

    if args.icon:
        with open('build/main.rc', 'w') as f:
            f.write(resource.replace('{icon}', args.icon))

    compiler = ccompiler.Compiler()
    compiler.libraries.extend(['Shell32', 'User32', 'PowrProf', 'Shlwapi'])
    compiler.sources = ['build/main.cpp']

    if args.icon:
        compiler.sources.append('build/main.rc')

    if not args.console:
        compiler.macros.append(('NO_CONSOLE', None))
        compiler.linker_postargs.append('/subsystem:windows')

    compiler.compile('build/main.exe')
    shutil.copy('build/main.exe', args.output)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'init':
        run_init(args)
    if args.command == 'build':
        run_build(args)
