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
using Leap.Unity.Attachments;

namespace IK
{
    /// <summary>
    /// Implementation of PCI_MuxIKDataProvider, specifically for IK with Leap Motion
    /// </summary>
    public class MuxIKDataProvider_LeapMotion : PCI_MuxIKDataProvider
    {
        /// <summary>
        /// Position transform
        /// </summary>
        private Transform tfLeap;
        /// <summary>
        /// IK hand transform, needed for the lerp
        /// </summary>
        private Transform tfIKHand;
        /// <summary>
        /// Active when the hand is seen by LeapMotion
        /// </summary>
        private bool fromTbToLeapMotion;
        /// <summary>
        /// Keep the previous frame information, if LeapMotion were active or not
        /// </summary>
        private bool previousLeapMotionInfo;
        private float timeStartLerp;
        private float secondsToStopLerp = 0.5f;

        /// <summary>
        /// AttachmentHand (Leap Motion class) from where it is obtained if it is being tracked or not 
        /// </summary>
        [SerializeField]
        private AttachmentHand attachmentHandToTrackStatus;

        private CameraPointer cameraPointer;

        public override void Awake()
        {
            base.Awake();
            tfLeap = transform;
            tfIKHand = muxIKController.transform;
            cameraPointer = FindObjectOfType<CameraPointer>();
        }

        /// <summary>
        /// Get the position where the IK target is going to point at
        /// </summary>
        /// <returns>Global position</returns>
        public override Vector3 GetIKPosition()
        {
            // Using tracker
            if (fromTbToLeapMotion)
            {
                if (Time.time - timeStartLerp > secondsToStopLerp)
                {
                    fromTbToLeapMotion = false;
                    return tfLeap.position;
                }
                return Vector3.Lerp(tfIKHand.position, tfLeap.position, Time.deltaTime * 20);
            }
            else
                return tfLeap.position;
        }

        private void Update()
        {
            if (cameraPointer && !cameraPointer.initialCalibrationDone)
                return;

            // There is a change, from TB to LeapMotion
            if (attachmentHandToTrackStatus.isTracked != previousLeapMotionInfo && attachmentHandToTrackStatus.isTracked)
            {
                fromTbToLeapMotion = true;
                timeStartLerp = Time.time;
            }

            previousLeapMotionInfo = attachmentHandToTrackStatus.isTracked;

            // If SetActive(true), LeapMotion is being used;
            //otherwise, LeapMotion is out of range, so TrackBand is providing position
            SetActive(attachmentHandToTrackStatus.isTracked);
        }

        public bool IsFromTbToLeapMotion()
        {
            return fromTbToLeapMotion;
        }
    }
}