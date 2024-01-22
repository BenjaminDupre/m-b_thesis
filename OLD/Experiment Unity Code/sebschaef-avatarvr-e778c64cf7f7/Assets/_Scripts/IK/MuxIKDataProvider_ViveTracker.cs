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

using UnityEngine;

namespace IK
{
    /// <summary>
    /// Implementation of PCI_MuxIKDataProvider, specifically for IK with Vive Trackers
    /// </summary>
    public class MuxIKDataProvider_ViveTracker : PCI_MuxIKDataProvider
    {
        /// <summary>
        /// Position transform
        /// </summary>
        private Transform tfTracker;

        [SerializeField]
        private bool fromTbToTracker;
        private bool previousTrackerInfo;
        private float timeStartReset;
        private float secondsToForgetReset = 0.5f;

        private Transform tfIKHand;

        [SerializeField]
        private SteamVR_Controller.Device steamDevice;

        public override void Awake()
        {
            base.Awake();
            tfTracker = transform;
            if (muxIKController)
                tfIKHand = muxIKController.transform;
        }

        /// <summary>
        /// Get the position where the IK target is going to point at
        /// </summary>
        /// <returns>Global position</returns>
        public override Vector3 GetIKPosition()
        {
            // Using tracker
            if (fromTbToTracker)
            {
                if (Time.time - timeStartReset > secondsToForgetReset)
                {
                    fromTbToTracker = false;
                    return tfTracker.position;
                }

                return Vector3.Lerp(tfIKHand.position, tfTracker.position, Time.deltaTime * 20);
            }
            else
                return tfTracker.position;


            //if (resetDetected)
            //    return avatarFKHandPosition.position;
            //else
            //    return ikTarget.position + deltaPosition;

            //return Vector3.Lerp(tfIKHand.position, tfTracker.position, Time.deltaTime * 20);

            //return tfTracker.position;
        }

        public void SetCurrentTracker(SteamVR_Controller.Device steamDevice)
        {
            this.steamDevice = steamDevice;
        }

        public void SetTfIKHand(Transform ikHand)
        {
            this.tfIKHand = ikHand;
        }

        private void Update()
        {
            if (steamDevice != null)
            {

                // There is a change, from TB to ViveTracker
                if (steamDevice.outOfRange != previousTrackerInfo && !steamDevice.outOfRange)
                {
                    fromTbToTracker = true;
                    //canPerformLerp = true;
                    timeStartReset = Time.time;
                }
                //else
                //    fromTBtoTracker = false;

                previousTrackerInfo = steamDevice.outOfRange;

                // If SetActive(true), ViveTracker is being used;
                //otherwise, ViveTracker is out of range, so TrackBand is providing position
                SetActive(!steamDevice.outOfRange);
            }
        }
    }
}