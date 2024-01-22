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

public class MUXDataProvider_ExternalVive : PCI_MuxDataProvider_ExternalChangeSource
{
    private const string viveSourceID = "vive";
    private SteamVR_Controller.Device steamDevice;
    private bool isUsingViveTracker = false;

    private Vector3 positionIK;
    private bool hasIKValues;

    public override void Start()
    {
        userId = 1;
    }

    public void StartAfterAssignment()
    {
        sourceId = viveSourceID;
        base.Start();
        ChangeGOName();
    }

    public void SetCurrentTracker(SteamVR_Controller.Device steamDevice)
    {
        this.steamDevice = steamDevice;
    }


    override public void SetIKPosition(Vector3 positionIK)
    {
        this.positionIK = positionIK;
        hasIKValues = true;
    }

    public override void CalculateHandPosition()
    {
        if (hasIKValues)
        {
            if (handModelController)
                SetMuxHandPosition(positionIK);
        }
        else
            base.CalculateHandPosition();

    }

    override public void Update()
    {
        base.Update();

        if (steamDevice != null)
        {
            // Lose tracker
            if (steamDevice.outOfRange)
            {
                // If tracker was being used, change to TB
                if (isUsingViveTracker)
                {
                    Debug.Log(steamDevice.index + ": Tracker -> TB");
                    changeSource = true;
                    isUsingViveTracker = false;
                }
            }
            // Tracker is visible
            else
            {
                // If tracker was not being used, change TB to tracker
                if (!isUsingViveTracker)
                {
                    Debug.Log(steamDevice.index + ": TB -> tracker");
                    changeSource = true;
                    isUsingViveTracker = true;
                }
            }
        }
    }

    private void ChangeGOName()
    {
        if (handLocation == NDAPIWrapperSpace.Location.LOC_RIGHT_HAND)
        {
            transform.name = "Controller (Right)";
        }
        else
        {
            transform.name = "Controller (Left)";
        }
    }
}
