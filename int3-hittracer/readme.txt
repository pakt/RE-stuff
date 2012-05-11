PoC implementation of an int3 tracer
------------------------------------

To verify that the  instrumentation doesn't introduce any lag:

debug.exe patched.exe <sample> 1000 0.0 10000 (terminates after 10s)

Files:

SumatraPDF.exe - version without instrumentation (no int3 patches)
patched.exe - instrumented version
debug.exe - debugger that's supposed to intercept and resume exceptions raised from patched.exe
urls.txt - urls of sample pdf files
stats.py - benchmarking script

The debugger takes few parameters:

<exe> <sample file> <dt> <c> <timeout>

where exe is the instrumented executable, sample file is the file to pass as a first parameter to the exe, dt is timestep, c is the cutoff constant S(t+dt)/S(t)>c, and timeout is the upper bound of time spent running the target (debugger will terminate the target, even when new BBs are still appearing). dt and timeout are in milliseconds, c is a float.



To benchmark:

- download the first 150 pdf files from urls.txt (scraped with Bing api ;)), delete 50 smallest ones, and place what's left in ./samples/ dir
- run SumatraPDF.exe and uncheck "Remember opened files" in Options (otherwise the results would be a bit skewed -- opening a file for the second time would trigger cache handling code)
- run stats.py and wait for results :)

More @ gdtr.wordpress.com
