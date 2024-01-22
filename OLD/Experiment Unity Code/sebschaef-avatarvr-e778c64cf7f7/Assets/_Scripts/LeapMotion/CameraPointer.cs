/******************************************************************************
* Copyright © NeuroDigital Technologies, S.L. 2018							  *
* Licensed under the Apache License, Version 2.0 (the "License");			  *
* you may not use this file except in compliance with the License.			  *
* You may obtain a copy of the License at 									  *
* http://www.apache.org/licenses/LICENSE-2.0								  *
* Unless required by applicable law or agreed to in writing, software		  *
* distributed under the License is distributed on an "AS IS" BASIS,			  *
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.	  *
* See the License for the specific language governing permissions and		  *
* limitations under the License.										      *
*******************************************************************************/

using NDAPIUnity;
using NDAPIWrapperSpace;
using UnityEngine;
using UnityEngine.UI;

public class CameraPointer : MonoBehaviour
{
    // RAYCAST
    public LayerMask layerMask = 1 << 0;
    private RaycastHit hit;
    private bool hasActivated;
    public float timeToActivate;
    private float timeElapsed;
    private Image progressBar;
    public bool initialCalibrationDone;

    // HAND MOTION CONTROLLERS AND HAPTIC CONTROLLER
    public HandModelController hmcR, hmcL;
    private HapticController hc;

    // SOUNDS
    private AudioSource loadingSound, activateSound;

    private void Awake()
    {
        loadingSound = GameObject.Find("Calib_loading_sound").GetComponent<AudioSource>();
        activateSound = GameObject.Find("Calib_activate_sound").GetComponent<AudioSource>();
    }

    // Use this for initialization
    void Start()
    {
        // Sets the progress bar as null
        progressBar = null;
        // Sets the hasActivated value to false to allow the player activates an option the first time
        hasActivated = false;

        initialCalibrationDone = false;
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        #region RAYCAST
        if (Physics.Raycast(this.transform.position, transform.TransformDirection(Vector3.forward), out hit, Mathf.Infinity, layerMask))
        {
            // If the progress bar is not null and has changed since las frame resets the timeElapsed and the hasActivated value. Otherwise, gets the new progress bar
            if (progressBar != null)
            {
                if (!progressBar.Equals(hit.collider.GetComponent<Image>()))
                {
                    timeElapsed = 0.0f;
                    hasActivated = false;
                    // Sets the new progress bar
                    progressBar = hit.collider.GetComponent<Image>();
                }
            }
            else
            {
                progressBar = hit.collider.GetComponent<Image>();
            }

            if (hit.collider.name.Equals("Calibrator") && !hasActivated)
            {
                if (IsTimeFinished())
                {
                    HapticController tempHCR, tempHCL;
                    // Gets each controller to know if the left and/or the right hand are connected
                    NDController.GetController(Location.LOC_RIGHT_HAND, out tempHCR);
                    NDController.GetController(Location.LOC_LEFT_HAND, out tempHCL);
                    // Calibrates the hands, the torso and the arms if they are not null
                    if (tempHCR != null)
                    {
                        if (hmcR != null)
                        {
                            hmcR.Recalibrate(true);
                            // If the right hand is a GloveOne, calibrates the flex sensors
                            hmcR.RecalibrateFlex();
                        }
                    }
                    if (tempHCL != null)
                    {
                        if (hmcL != null)
                        {
                            hmcL.Recalibrate(true);
                            // If the left hand is a GloveOne, calibrates the flex sensors
                            hmcL.RecalibrateFlex();
                        }
                    }

                    // If calibration is done, show hands and arms and delete calibration objects
                    if (!initialCalibrationDone)
                        EnableInitialCalibration();
                }
            }
        }
        else
        {
            // Resets the progress bar
            if (progressBar != null)
            {
                progressBar.fillAmount = 0.0f;
            }
            progressBar = null;
            timeElapsed = 0.0f;
            // Sets hasActivated to false, so the player can activate any option again
            hasActivated = false;
            // Stop the loading sound
            loadingSound.Stop();
        }
        #endregion
    }

    private void EnableInitialCalibration()
    {
        initialCalibrationDone = true;
    }

    /// <summary>
    /// Controls if the player has been looking for the time needed to activate the buttons.
    /// </summary>
    /// <returns><c>true</c> if the time elapsed is greater than the time needed to activate; otherwise, <c>false</c>.</returns>
    bool IsTimeFinished()
    {
        // Plays the loading sound just once
        if (!loadingSound.isPlaying)
        {
            loadingSound.Play();
        }

        // Increases the timeElapsed value each frame
        timeElapsed += Time.deltaTime;
        // If there's a progress bar, increases the fillAmount to perform a loading effect
        if (progressBar != null)
        {
            progressBar.fillAmount = timeElapsed / timeToActivate;
        }

        if (timeElapsed >= timeToActivate)
        {
            // Stops the loading sound
            loadingSound.Stop();
            // Plays the activated sound
            activateSound.PlayOneShot(activateSound.clip);
            // Resets the progressBar fillAmount
            progressBar.fillAmount = 0.0f;
            // Resets the timeElapsed
            timeElapsed = 0.0f;
            // Sets hasActivated to true to make the player look at another point if he/she wants to activate the option again
            hasActivated = true;

            return true;
        }
        else
        {
            return false;
        }
    }
}
