using System;
using System.Collections.Generic;

namespace System.Threading.Tasks
{
    public static class TaskUtilities
    {
        public static Task StartNew(Action action)
        {
            return Task.Factory.StartNew(action, CancellationToken.None, TaskCreationOptions.None, TaskScheduler.Default);
        }

        public static Task<TResult> StartNew<TResult>(Func<TResult> func)
        {
            return Task.Factory.StartNew<TResult>(func, CancellationToken.None, TaskCreationOptions.None, TaskScheduler.Default);
        }

        public static Task StartNew(Action action, CancellationToken ct)
        {
            return Task.Factory.StartNew(action, ct, TaskCreationOptions.None, TaskScheduler.Default);
        }

        public static Task<TResult> StartNew<TResult>(Func<TResult> func, CancellationToken ct)
        {
            return Task.Factory.StartNew<TResult>(func, ct, TaskCreationOptions.None, TaskScheduler.Default);
        }
    }
}
