
using UnityEngine;
using System.Collections;
using System.IO.Ports;
using System.IO;
using System;
using System.Threading;

public class Post_heartIntroceptive : MonoBehaviour
{

    SerialPort stream = new SerialPort("\\\\.\\COM21", 115200); //Set the port (com4) and the baud rate (9600, is standard on most devices)
    float valuex = 0f;

    StreamWriter streamWriter;
    Thread thread;
    bool isLogging = true;
    bool isCounting1Minute = false;
    float timer;

    public string ParticipantID;
    public string IntroLogDir = "D:/PostExperimentIntroceptiveLog/";
    private string LogStartingTimeID;

    public AudioClip impact;
    AudioSource audioSource;


    // Start is called before the first frame update
    void Start()
    {
        LogStartingTimeID = DateTime.Now.ToString("yyyyMMdd_HH.mm.ss_ffffff");
        audioSource = GetComponent<AudioSource>();

        timer = 60f;

        thread = new Thread(Log);
        thread.Start();

    }

    // Update is called once per frame
    void Update()
    {
        if (timer >= 0 && isCounting1Minute == true)
        {
            timer -= Time.deltaTime;
            Debug.Log(timer);
        }

        if (timer < 0 && isCounting1Minute == true)
        {
            streamWriter.WriteLine(DateTime.Now.ToString("HH:mm:ss.ffffff") + ";" + 88888888 + ";");

            isCounting1Minute = false;
            audioSource.PlayOneShot(impact, 0.7F);

        }

        if (Input.GetKeyDown("space"))
        {
            timer = 60f;
            isCounting1Minute = true;
            streamWriter.WriteLine(DateTime.Now.ToString("HH:mm:ss.ffffff") + ";" + 99999999 + ";");
            audioSource.PlayOneShot(impact, 0.7F);
        }
    }
    private void OnApplicationQuit()
    {
        isLogging = false;
        while (thread.IsAlive) ;
    }

    private void Log()
    {
        stream.Open();
        streamWriter = new StreamWriter(IntroLogDir + ParticipantID + "_" + LogStartingTimeID + "_IntroceptiveLog.csv");
        streamWriter.WriteLine("ComputerClockFromUnity" + ";" + "TimeElapsedArduinoBeginInMicroSec" + ";" + "DatapointRunningNumber" + ";" + "Voltage" + ";" + "QRS");
        while (isLogging)
        {
            string value = stream.ReadLine(); //Read the information


            try
            {
                //valuex = float.Parse(value);

                Debug.Log(value);

                streamWriter.WriteLine(DateTime.Now.ToString("HH:mm:ss.ffffff") + ";" + value);
            }
            catch (Exception e) { }
            //Thread.Sleep(1);
        }

        streamWriter.Flush();
        streamWriter.Close();
    }

}



