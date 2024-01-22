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
using IK;

public class GhostAvatarController : MonoBehaviour
{
    public NDAnimationPlayer animPlayer;
    public ShowHideRoboticMesh shrm;
    public MuxIKDataProvider_LeapMotion muxIKDPLeapLeft, muxIKDPLeapRight;
    private CameraPointer cameraPointer;
    private FollowVRCam followVRCam;

    void Awake()
    {
        followVRCam = FindObjectOfType<FollowVRCam>();
        cameraPointer = FindObjectOfType<CameraPointer>();
    }

    // Update is called once per frame
    void Update()
    {
        if (!muxIKDPLeapLeft && !muxIKDPLeapRight)
            return;

        if (cameraPointer)
        {
            if (cameraPointer.initialCalibrationDone)
            {
                if (!animPlayer.IsAnimationFinished())
                    animPlayer.PlayAnimation();
            }
        }

        if ((muxIKDPLeapLeft && muxIKDPLeapLeft.IsFromTbToLeapMotion()) || (muxIKDPLeapRight && muxIKDPLeapRight.IsFromTbToLeapMotion()))
        {
            if (shrm)
            {
                shrm.ShowActiveHands();
                shrm.ShowActiveArms();
                shrm.ShowChest();
            }

            if (followVRCam)
                followVRCam.readyToMove = true;
            Destroy(gameObject);
        }
        else
        {
            shrm.HideChest();
            shrm.HideActiveHands();
            shrm.HideActiveArms();
        }
    }
}
