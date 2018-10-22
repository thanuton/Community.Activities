﻿using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;

namespace System
{
    public static class Extensions
    {
        public static bool IsNullOrEmpty(this string value)
        {
            return string.IsNullOrEmpty(value);
        }

        public static IComparer<T> ToComparer<T>(this Func<T, T, int> compare)
        {
            return new Comparer<T>(compare);
        }

        private class Comparer<T> : IComparer<T>
        {
            private Func<T, T, int> _compare;
            public Comparer(Func<T, T, int> comparison)
            {
                _compare = comparison;
            }
            public int Compare(T x, T y)
            {
                return _compare(x, y);
            }
        }

        public static KeyValuePair<TKey, TValue> ToKeyValue<TKey, TValue>(this TKey key, TValue value)
        {
            return new KeyValuePair<TKey, TValue>(key, value);
        }

        public static IDisposable DisposeWith<T>(this T obj, Action<T> onDispose, out T outObj)
        {
            outObj = obj;
            return DisposeWith(obj, onDispose);
        }

        public static IDisposable DisposeWith<T>(this T obj, Action<T> onDispose)
        {
            if (obj == null)
            {
                return Disposable.Empty;
            }
            return new Disposable(() => onDispose(obj));
        }

        public static IDisposable DisposeWithReleaseComObject<T>(this T obj, out T outObj)
        {
            return DisposeWith(obj, (onDispose) => Marshal.ReleaseComObject(obj), out outObj);
        }

        public static IDisposable DisposeWithReleaseComObject<T>(this T obj)
        {
            return DisposeWith(obj, (onDispose) => Marshal.ReleaseComObject(obj));
        }

        private class Disposable : IDisposable
        {
            public static Disposable Empty = new Disposable(null) { _disposed = true };
            private Action _onDispose;
            public Disposable(Action onDispose)
            {
                _onDispose = onDispose;
            }

            private bool _disposed;
            public void Dispose()
            {
                if (_disposed)
                {
                    return;
                }
                _onDispose?.Invoke();
                _disposed = true;
            }
        }
    }
}

namespace System.Collections.Generic
{
    public static class Extensions
    {
        public static bool IsNullOrEmpty<T>(this IEnumerable<T> source)
        {
            return source == null || !source.Any();
        }

        public static bool IsNullOrEmpty<T>(this ICollection<T> source)
        {
            return source == null || source.Count == 0;
        }

        public static IEnumerable<T> EmptyIfNull<T>(this IEnumerable<T> source)
        {
            return source ?? Enumerable.Empty<T>();
        }

        public static IOrderedEnumerable<T> OrderBy<T, TKey>(this IEnumerable<T> source, Func<T, TKey> keySelector, Func<TKey, TKey, int> compare)
        {
            return source.OrderBy(keySelector, compare.ToComparer());
        }

        public static IOrderedEnumerable<T> OrderByDescending<T, TKey>(this IEnumerable<T> source, Func<T, TKey> keySelector, Func<TKey, TKey, int> compare)
        {
            return source.OrderByDescending(keySelector, compare.ToComparer());
        }

        public static TValue Get<TKey, TValue>(this IDictionary<TKey, TValue> source, TKey key)
        {
            if (source.TryGetValue(key, out TValue value))
            {
                return value;
            }
            return default(TValue);
        }

        public static TValue? GetValue<TKey, TValue>(this IDictionary<TKey, TValue> source, TKey key)
            where TValue : struct
        {
            if (source.TryGetValue(key, out TValue value))
            {
                return value;
            }
            return null;
        }
    }
}

namespace System.IO
{
    public static class Extensions
    {
        public static byte[] ReadToEnd(this Stream stream, int chunkSize = 1024)
        {
            if (stream == null)
            {
                return new byte[0];
            }
            if (stream.CanSeek)
            {
                long size = stream.Length - stream.Position;

                if (size < int.MaxValue)
                {
                    chunkSize = (int)size;
                }
            }

            byte[] result = new byte[0];
            byte[] buffer = new byte[chunkSize];
            int read = 0;

            while ((read = stream.Read(buffer, 0, chunkSize)) > 0)
            {
                int resultLength = result.Length;

                Array.Resize(ref result, resultLength + read);
                Array.Copy(buffer, 0, result, resultLength, read);
            }

            return result;
        }
    }
}

namespace System.Threading.Tasks
{
    public static class TaskExtensions
    {
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Usage", "CA1801:ReviewUnusedParameters", MessageId = "task")]
        public static void DoNotAwait(this Task task)
        {

        }
    }
}