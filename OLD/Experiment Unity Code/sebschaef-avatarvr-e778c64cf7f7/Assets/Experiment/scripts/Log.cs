using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.IO.Ports; // From Merts script
using System.Text;
using System.Threading;
using UnityEngine;


public class Log : MonoBehaviour
{
// Merts script
    SerialPort stream = new SerialPort("\\\\.\\COM21", 9600); //Set the port (com4) and the baud rate (9600, is standard on most devices)
    // Changes by Tim: comment the line above, uncomment the line below to use my Arduino device.
    //SerialPort stream = new SerialPort("\\\\.\\COM23", 115200); //Set the port (com4) and the baud rate (9600, is standard on most devices)
    public GameObject heartbeat;
    new Vector3 posheart;
    float valuex = 0f;

    StreamWriter streamWriter;
    Thread thread;
    bool isLogging = true;
    public string LogDir;
 // Merts script

    public int loggingIntervalInMs = 7; 

    public GameObject tutorialGrabBall;
    public GameObject tutorialCalibrate;
    public GameObject head;

    private static string metaHeaders = "timeCreated;age;handedness;name";
    private static string levelHeaders = "time;Milliseconds;levelCounter;correctCounter;leftHandPosition;leftHandRotation;" +
        "rightHandPosition;rightHandRotation;redBallPosition;redBallRotation;" +
        "leftHandGrab;rightHandGrab;feedbackType;leftHandVibration;rightHandVibration;" +
        "correctBallPosition;lastTemplateBallPosition;areCalibratingGhostHandsActive;" +
        "areGrabbingGhostHandsActive;calibrationState;isCalibrationBlocked;" +
        "grabbingState;buttonHasBeenPressed;buttonCurrentlyPressed;headPosition;headRotation;" +
        "value"; //You can add the QRs here too if you like

    private string rootDirectory = "C:/Participants/";
    private string participantDirectory = "Undefined participant";
    public string LogDirectory;



    private StreamWriter levelStreamWriter;
    public Thread levelThread;

    private bool stopLevelLoggingThread = false;

    private GameObject leftHand, rightHand;
    private Vector3 leftHandPos, rightHandPos;
    private Vector3 leftHandRot, rightHandRot;
    private Vector3 headPos, headRot;

    private GameObject redBall;
    private Vector3 redBallPos, redBallRot;

    private ObjectDetector leftHandObjDetector, rightHandObjDetector;

    private BallSpawnController ballSpawnController;
    private LevelBehaviour levelBehaviour;
    private ButtonBehaviour buttonBehaviour;

    private bool areGrabbingGhostHandsActive = false;
    private bool areCalibrationGhostHandsActive = false;

    private int levelCounter = 1;

    private void Start()
    {

        GameObject eventSystem = GameObject.Find("EventSystem");
        ballSpawnController = eventSystem.GetComponent<BallSpawnController>();
        levelBehaviour = eventSystem.GetComponent<LevelBehaviour>();
        buttonBehaviour = levelBehaviour.button.GetComponent<ButtonBehaviour>();

        // Merts script
        GameObject thePlayer = GameObject.Find("EventSystem");
        LogDir = thePlayer.GetComponent<Log>().LogDirectory;
        Debug.Log(LogDir + "YAZDIMMM");
        thread = new Thread(Logging);
        thread.Start();
        //Open the Serial Stream.
        //stream.ReadTimeout = 1;
        // Merts script
    }

    private void Update()
    {
       // StartCoroutine(MyCoroutine()); // Added by Tim

        if (leftHand == null)
        {
            leftHand = GameObject.Find("IMU_hand_l");
        }
        else
        {
            leftHandPos = leftHand.transform.position;
            leftHandRot = leftHand.transform.rotation.eulerAngles;
        }

        if (rightHand == null)
        {
            rightHand = GameObject.Find("IMU_hand_r");
        }
        else
        {
            rightHandPos = rightHand.transform.position;
            rightHandRot = rightHand.transform.rotation.eulerAngles;
        }

        redBall = GameObject.Find("redBall_noVibration Variant Drop(Clone)");
        if (redBall != null)
        {
            redBallPos = redBall.transform.position;
            redBallRot = redBall.transform.rotation.eulerAngles;
        }

        leftHandObjDetector = levelBehaviour.leftHand.GetComponentInChildren<ObjectDetector>();
        rightHandObjDetector = levelBehaviour.rightHand.GetComponentInChildren<ObjectDetector>();

        headPos = head.transform.position;
        headRot = head.transform.rotation.eulerAngles;

        areCalibrationGhostHandsActive = tutorialCalibrate.activeSelf;
        areGrabbingGhostHandsActive = tutorialGrabBall.activeSelf;
    }

    private void OnApplicationQuit()
    {
        Debug.Log("Waiting for Logging to finish..");
        StopFullLogging();
        while (levelThread.IsAlive) ;
        Debug.Log("Logging finished. Quitting..");
        // Merts script
            isLogging = false;
            while (thread.IsAlive) ;
        // Merts script
    }


    public void Init(string rootDirectory)
    {
        this.rootDirectory = rootDirectory;
        this.participantDirectory = GetNextParticipantDirectoryNumber(rootDirectory);

        Directory.CreateDirectory(rootDirectory + participantDirectory + "levels/");
        Debug.Log("Created new Participant directory: " + rootDirectory + participantDirectory);

        LogDirectory = rootDirectory + participantDirectory;
        Debug.Log("this is the public LogDirectory" + LogDirectory);


        //Debug.Log(thePlayer.GetComponent<heartbeatlog>().LogDir + "YAZDIMMM");


        createMetaFile();
        Debug.Log("Created the META.CSV");
    }

    private string GetNextParticipantDirectoryNumber(string rootDirectory)
    {
        string[] dirs = Directory.GetDirectories(rootDirectory);

        int highestParticipantNumber = -1;
        foreach (string dir in dirs)
        {
            string[] pathSplit = dir.Split('/');
            int dirNum = int.Parse(pathSplit[pathSplit.Length - 1]);
            if (dirNum > highestParticipantNumber)
                highestParticipantNumber = dirNum;
        }

        return (++highestParticipantNumber).ToString("D2") + "/";
    }

    private void createMetaFile()
    {
        using (StreamWriter metaStreamWriter = new StreamWriter(rootDirectory + participantDirectory + "meta.csv"))
        {
            metaStreamWriter.WriteLine(metaHeaders);
            metaStreamWriter.Write(CurrentDateTime());

            string emptyColumnsString = "";
            foreach (char c in metaHeaders)
            {
                if (c == ';')
                    emptyColumnsString += ";";
            }
            metaStreamWriter.WriteLine(emptyColumnsString);

            metaStreamWriter.Flush();
            metaStreamWriter.Close();
        }
    }

    private string CurrentDateTime()
    {
        return DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
    }

    private byte[] ToUtf8ByteArray(string text)
    {
        return new UTF8Encoding(true).GetBytes(text);
    }

    public void PrepareLevelLogFiles()
    {
        // Nothing to do here at the moment
    }

    public void StartFullLogging()
    {
        stopLevelLoggingThread = false;
        levelThread = new Thread(ThreadedFullLogging);
        levelThread.Start();
    }

    public void StopFullLogging()
    {
        stopLevelLoggingThread = true;
    }

    private void ThreadedFullLogging()
    {
        levelStreamWriter = new StreamWriter(rootDirectory + participantDirectory + "everything.csv");
        levelStreamWriter.WriteLine(levelHeaders);

        while (!stopLevelLoggingThread)
        {
            LogLine logLine = new LogLine();
            logLine.Add(CurrentDateTime());

           // logLine.Add(DateTime.millisecond());
            logLine.Add(DateTime.UtcNow.Millisecond.ToString());

            if (levelBehaviour != null)
            {
                logLine.Add(levelBehaviour.levelCounter.ToString());
                logLine.Add(levelBehaviour.correctCounter.ToString());
            }
            else
            {
                logLine.SkipFields(2);
            }

            if (leftHandPos != null && leftHandRot != null)
            {
                logLine.Add(leftHandPos.ToString());
                logLine.Add(leftHandRot.ToString());
            }
            else
            {
                logLine.SkipFields(2);
            }

            if (rightHandPos != null && rightHandRot != null)
            {
                logLine.Add(rightHandPos.ToString());
                logLine.Add(rightHandRot.ToString());
            }
            else
            {
                logLine.SkipFields(2);
            }

            if (redBallPos != null && redBallRot != null)
            {
                logLine.Add(redBallPos.ToString());
                logLine.Add(redBallRot.ToString());
            }
            else
            {
                logLine.SkipFields(2);
            }

            if (leftHandObjDetector != null)
                logLine.Add(leftHandObjDetector.isGrabbing.ToString());
            else
                logLine.SkipField();

            if (rightHandObjDetector != null)
                logLine.Add(rightHandObjDetector.isGrabbing.ToString());
            else
                logLine.SkipField();

            if (ballSpawnController != null)
            {
                string feedbackType = "";
                switch (ballSpawnController.feedbackType)
                {
                    case BallSpawnController.FeedbackType.NONE:
                        feedbackType = "none";
                        break;
                    case BallSpawnController.FeedbackType.CONGRUENT:
                        feedbackType = "congruent";
                        break;
                    case BallSpawnController.FeedbackType.INCONGRUENT:
                        feedbackType = "incongruent";
                        break;
                }
                logLine.Add(feedbackType);
                logLine.Add(ballSpawnController.isLeftHandVibrating.ToString());
                logLine.Add(ballSpawnController.isRightHandVibrating.ToString());
            }
            else
            {
                logLine.SkipFields(3);
            }

            if (levelBehaviour != null)
            {
                Vector2Int ballCoord = new Vector2Int(
                    levelBehaviour.GetCurrentBallPosition() % 6,
                    levelBehaviour.GetCurrentBallPosition() / 6
                );

                logLine.Add(ballCoord.ToString());
            }
            else
            {
                logLine.SkipField();
            }

            logLine.Add(TemplateSphereBehaviour.lastBallPosition.ToString());

            logLine.Add(areCalibrationGhostHandsActive.ToString());
            logLine.Add(areGrabbingGhostHandsActive.ToString());

            if (levelBehaviour != null)
            {
                logLine.Add(levelBehaviour.calibrationState.ToString("g"));
                logLine.Add(levelBehaviour.isCalibrationBlocked.ToString());
                logLine.Add(levelBehaviour.grabbingState.ToString("g"));
            }
            else
            {
                logLine.SkipFields(3);
            }

            if (buttonBehaviour != null)
            {
                logLine.Add(buttonBehaviour.hasBeenPressed.ToString());
                logLine.Add(buttonBehaviour.isPressing.ToString());
            }
            else
            {
                logLine.SkipFields(2);
            }

            if (headPos != null)
                logLine.Add(headPos.ToString());
            else
                logLine.SkipField();

            if (headRot != null)
                logLine.Add(headRot.ToString());
            else
                logLine.SkipField();

            // Begin Merts Code
                 if (isLogging == false)
                isLogging = true;
            // thread.Start();
            //if (stream.IsOpen == false)
                      // stream = null;
           // stream.Open();
            
            if (stream == null || !stream.IsOpen)
            while (isLogging && stream.IsOpen == true)
             if (stream.IsOpen == false)
              {
                  thread.Start();
               }
            // else

            // Begin Merts Code
            if (stream.IsOpen == true)
            {
                string value = stream.ReadLine(); //Read the information defined by the Arduino Output. Voltage as an essential, but if you like also the QRS decision, elapsed time or whatever
                string QRS = value; // Needs changes. the data needs to be splitted then
                    try
                {
                    //valuex = float.Parse(value);

                    Debug.Log(value); // Comment from Tim. I don't remember what us in "value" it is either the voltage which is most important, or the whole bunch of information like QRS decision too.

                }
                catch (Exception e) { }
                //Thread.Sleep(1);

                // End Merts Code
                logLine.Add(value.ToString()); // Code from Tim /This line is important. Depending what data you transfer in stream.Readline, this logline adds it to the csv. file so if you transfer above als "QRS" or "TimeElapsedArduinoBeginInMicroSec" write something like
                                               //logLine.Add(TimeElapsedArduinoBeginInMicroSec.ToString()); // Comment, not working yet, you need to define this variable first and read it in before you can save it.
                                               //logLine.Add(QRS.ToString());// Comment, not working yet, you need to define this variable first and read it in before you can save it.
                //logLine.Add(QRS.ToString());
                }

                levelStreamWriter.WriteLine(logLine);
                // Thread.Sleep(loggingIntervalInMs); // Something is wrong here



        }
    }

    // Changes
   // IEnumerator MyCoroutine()
  //  {
   //     yield return new WaitForSeconds(0.0075F);
        //yield return new WaitForSeconds(0.75F);

  //  }
    // Changes


    private class LogLine
    {
        private string line;

        public LogLine()
        {
            line = "";
        }

        public string Add(string field)
        {
            if (!String.IsNullOrEmpty(line))
            {
                line += ";";
            }

            line += field;
            return line;
        }

        public string SkipField()
        {
            return SkipFields(1);
        }

        public string SkipFields(int amount)
        {
            for (int i = 0; i < amount; i++)
            {
                line += ";";
            }

            return line;
        }

        public override string ToString()
        {
            return line;
        }
    }
    // Merts Code
    private void Logging() //Changing Log to logging due to double uase in this script
    {
        stream.Open();
        //streamWriter = new StreamWriter(LogDir + "heartrate.csv");
        //streamWriter.WriteLine("ComputerClockFromUnity" + ";" + "TimeElapsedArduinoBeginInMicroSec" + ";" + "DatapointRunningNumber" + ";" + "Voltage" + ";" + "QRS");
        while (isLogging)
        {
            string value = stream.ReadLine(); //Read the information


            try
            {
                //valuex = float.Parse(value);

                Debug.Log(value);

                //streamWriter.WriteLine(DateTime.Now.ToString("HH:mm:ss.ffffff") + ";" + value);
            }
            catch (Exception e) { }
            //Thread.Sleep(1);
            streamWriter.Flush();
        }

        
        //streamWriter.Close();
    }
    // Merts Code
}
