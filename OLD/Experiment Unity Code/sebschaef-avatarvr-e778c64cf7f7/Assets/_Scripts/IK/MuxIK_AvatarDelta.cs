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
    /// Implementation of PCI_MuxIKDataProvider. This component allows to use AvatarVR from the last known point of Leap Motion.
    /// </summary>
    public class MuxIK_AvatarDelta : PCI_MuxIKDataProvider
    {
        /// <summary>
        /// Event that is triggered when the device is reseted
        /// </summary>
        [SerializeField]
        private SO_TriggerEvent soOnAvatarResetEvent;

        /// <summary>
        /// IK target transform
        /// </summary>
        [SerializeField]
        private Transform ikTarget;
        /// <summary>
        /// Avatar FK hand position
        /// </summary>
        private Transform avatarFKHandPosition;
        /// <summary>
        /// If this property is true, the device is reseted
        /// </summary>
        public bool resetDetected;

        private Vector3 lastPosition;
        private Vector3 deltaPosition;

        private float timeStartReset;
        private float secondsToForgetReset = 1;

        public override void Awake()
        {
            base.Awake();
            avatarFKHandPosition = transform;

            lastPosition = avatarFKHandPosition.position;

            soOnAvatarResetEvent.Register(ResetDetected);
        }


        private void OnDestroy()
        {
            soOnAvatarResetEvent.Unregister(ResetDetected);
        }

        /// <summary>
        /// Method to trigger
        /// </summary>
        public void ResetDetected()
        {
            timeStartReset = Time.time;
            resetDetected = true;
        }

        /// <summary>
        /// Calculate the deltaPosition given by AvatarVR
        /// </summary>
        /// <returns>World position of the IK target</returns>
        public override Vector3 GetIKPosition()
        {
            deltaPosition = (avatarFKHandPosition.position - lastPosition);
            lastPosition = avatarFKHandPosition.position;

            if (resetDetected)
                if (Time.time - timeStartReset > secondsToForgetReset)
                    resetDetected = false;

            if (resetDetected)
                return avatarFKHandPosition.position;
            else
                return ikTarget.position + deltaPosition;
        }

        /// <summary>
        /// Check if reset has been done and return if it is using Lerp or not.
        /// </summary>
        /// <returns>True if lerp is active; false otherwise.</returns>
        public override bool UseLerp()
        {
            if (resetDetected)
            {
                if (Vector3.Distance(avatarFKHandPosition.position, ikTarget.position) < 0.001f)
                    resetDetected = false;
            }

            return base.UseLerp();
        }

        /// <summary>
        /// Set this MuxIKDataProvider as active.
        /// </summary>
        /// <param name="hasBeenPickedByMux">If true, take data from this MuxIKDataProvider</param>
        public override void NewPickedByMuxStatus(bool hasBeenPickedByMux)
        {
            if (hasBeenPickedByMux)
                lastPosition = avatarFKHandPosition.position;
        }
    }
}
