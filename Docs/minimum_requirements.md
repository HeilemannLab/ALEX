## Minimum requirements

1. Menue item __Save settings__:
   * lets the user select a directory
   * saves settings of the interface into _.txt_ and _.p_

2. Menue item __Load settings__:
   * lets the user select a file
   * reads the dictionary from the file and sets the interface to its values
   * does make clear that only _.p_ files can be selected

3. Menue item __Convert to photon-HDF5__:
   * lets the user select a directory
   * warns if there are no measurement files that can be converted
   * shows _hdf info mask_ again
   * when the _hdf info mask_ is terminated without save, either convertion must be halted or just the original info file used (it is the second option at the moment)
   * correct rollover in both files
   * merge and sort timestamp arrays and write to a new file named _smALEX.hdf_ in the same folder
   * all hdf info and also illumination period info must be saved

4. Menue item __Close__ closes all open windows

5. __Browse__ button lets the user select a directory, where the measurement folders will be located

6. The QLineEdit associated with __Browse__:
   * displays the chosen directory (it is read-only)
   * gives proper hint to the use of __Browse__

7. __Laserpower__ sliders and boxes:
   * are tunable and interact with each other
   * laser power settings are actually transmitted to the AOTF

8. __Ratio__ slider and boxes:
   * are tunable and interact with each other
   * ratio setting is actually displayed in the illumination pattern

9. The _silencing pulses_ fit to the illumination pattern

10. __ALEX frequency__ box lets the user change the frequency with that the illumination pattern will be repeated

11. __Measurement duration__ box lets the user chose a duration between 1 and 300 seconds

12. __Measurement mode__ radio buttons can be clicked and interact with each other

13. __Count rates__ LCD panels show the counted rates during the measurement

14. __ProgressBar__:
    * in _Finite_: show the progress until measurement duration elapsed
    * in _Continuous_: show running thing (?)

15. __StatusBar__ shows nice and helpful messages

16. __Start__ button:
    * In _Finite_:
      * show the _hdf info mask_
      * save interface settings and hdf info in a folder named _sample+date+time_
      * start the measurement
      * show the data in the animation window
      * save the data in a _.hdf_ file in the same folder

    * In _Continuous_:
      * start the measurement
      * show the data in the animation window
17. __Stop__ button stops the measurement any time

18. _Digital signals_, _Analog signals_ and _Counting_ start synchronized

19. In _Finite_ mode data is retrieved and saved precisley as long as the specified _Measurement duration_

20. 