﻿using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using UiPath.Python.Impl;
using UiPath.Python.Properties;

namespace UiPath.Python
{
    /// <summary>
    /// class providing the Python corresponding engine based on version/path
    /// </summary>
    public static class EngineProvider
    {
        private const string PythonHomeEnv = "PYTHONHOME";
        private const string PythonExe = "python.exe";

        // engines cache
        private static object _lock = new object();
        private static Dictionary<Version, IEngine> _cache = new Dictionary<Version, IEngine>();

        public static IEngine Get(Version version, string path, bool inProcess = true, TargetPlatform target = TargetPlatform.x86, bool visible = false)
        {
            IEngine engine = null;
            lock (_lock)
            {
                if (string.IsNullOrEmpty(path))
                {
                    // read path from env variable
                    path = Environment.GetEnvironmentVariable(PythonHomeEnv);
                    Trace.TraceInformation($"Found Pyhton path {path}");
                }

                if (!version.IsValid())
                {
                    Autodetect(path, out version);
                    if (!version.IsValid())
                    {
                        throw new ArgumentException(Resources.DetectVersionException);
                    }
                }

                // TODO: target&visible are meaningless when running in-process (at least now), maybe it should be split
                if(inProcess)
                {
                    if (!_cache.TryGetValue(version, out engine))
                    {
                        engine = new Engine(version, path);
                    }
                    _cache[version] = engine;
                }
                else
                {
                    // TODO: do we need caching when running as service (out of process)?
                    engine = new OutOfProcessEngine(version, path, target, visible);
                }
            }
            return engine;
        }

        private static void Autodetect(string path, out Version version)
        {
            Trace.TraceInformation($"Trying to autodetect Python version from path {path}");
            string pyExe = Path.GetFullPath(Path.Combine(path, PythonExe));
            if (!File.Exists(pyExe))
            {
                throw new FileNotFoundException(Resources.PythonExeNotFoundException, pyExe);
            }

            version = FileVersionInfo.GetVersionInfo(pyExe).Get();
            Trace.TraceInformation($"Autodetected Python version {version}");
        }
    }
}
