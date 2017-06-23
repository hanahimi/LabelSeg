@echo off

set path_a="LOC_configUG-SAIC.cfg"
set path_b="..\COMM\Data\Config\LOC_configUG-SAIC.cfg"

for %%i in (%path_a%) do set time_a=%%~ti
for %%i in (%path_b%) do set time_b=%%~ti
echo time of %path_a% : %time_a%
echo time of %path_b% : %time_b%

if "%time_a%" gtr "%time_b%" (
  echo %path_a% is new
  copy %path_a% %path_b%
) else (
  echo %path_b% is new
  copy %path_b% %path_a%

)

pause