using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallDroppedBehaviour : MonoBehaviour
{
    public float ballDroppedYThreshold = 0.1f;
    public GameObject eventSystem;

    private void Start()
    {
        eventSystem = GameObject.Find("EventSystem");
    }

    void FixedUpdate()
    {
        if (gameObject.transform.position.y <= ballDroppedYThreshold)
        {
            eventSystem.GetComponent<LevelBehaviour>().OnBallDropped();
            Destroy(gameObject);
        }
    }
}
