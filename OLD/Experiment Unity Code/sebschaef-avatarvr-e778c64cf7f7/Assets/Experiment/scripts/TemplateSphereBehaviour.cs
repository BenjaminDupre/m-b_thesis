using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TemplateSphereBehaviour : MonoBehaviour
{
    public GameObject eventSystem;
    public GameObject wrongExplosion, rightExplosion;

    public float timeUntilExplosion = 1f;
    public float timeUntilRestart = 2f;

    private GameObject collidingBall;

    private Vector3 colliderSize, colliderTopLeft;
    private LevelBehaviour levelBehaviour;

    private bool isExplosionTriggered = false;

    public static Vector2Int lastBallPosition = new Vector2Int(-1, -1);

    private void Start()
    {
        levelBehaviour = eventSystem.GetComponent<LevelBehaviour>();
        colliderSize = GetComponent<Collider>().bounds.size;
        colliderTopLeft = transform.position - colliderSize / 2f;
    }

    private void OnTriggerEnter(Collider collider)
    {
        if (collider.gameObject.layer == LayerMask.NameToLayer("Grabbable"))
        {
            int currBallPosition = levelBehaviour.GetCurrentBallPosition();
            int currGridSize = levelBehaviour.gridSize;

            Vector3 ballCoordinates = collider.gameObject.transform.position;

            // TODO adapt to different widths and heights.
            float stepX = colliderSize.x / 6;
            float stepZ = colliderSize.z / 3;

            Vector2Int correctBallPosition = new Vector2Int(
                currBallPosition % 6,
                2 - (currBallPosition / 6) // inverted grid
            );

            collidingBall = collider.gameObject;

            lastBallPosition = new Vector2Int(
                (int) ((ballCoordinates.x - colliderTopLeft.x) / stepX),
                (int) ((ballCoordinates.z - colliderTopLeft.z) / stepZ)
            );

            if (isExplosionTriggered || collidingBall.GetComponent<Rigidbody>().isKinematic)
                return;

            isExplosionTriggered = true;
            Debug.Log(correctBallPosition + ", " + lastBallPosition);

            if (lastBallPosition.Equals(correctBallPosition))
                Invoke("OnCorrectCollidingBall", timeUntilExplosion);
            else
                Invoke("OnWrongCollidingBall", timeUntilExplosion);
        }
    }

    private void OnCorrectCollidingBall()
    {
        if (collidingBall == null) // Sometimes the collision gets triggered a second time.
            return;

        Instantiate(wrongExplosion, collidingBall.transform.position, Quaternion.identity);
        Destroy(collidingBall);
        eventSystem.GetComponent<LevelBehaviour>().OnBallPlacedCorrectly();
        Invoke("LevelFinished", timeUntilRestart);
        isExplosionTriggered = false;
    }

    private void OnWrongCollidingBall()
    {
        if (collidingBall == null)
            return;

        Instantiate(wrongExplosion, collidingBall.transform.position, Quaternion.identity);
        Destroy(collidingBall);
        eventSystem.GetComponent<LevelBehaviour>().OnBallPlacedWrong();
        Invoke("LevelFinished", timeUntilRestart);
        isExplosionTriggered = false;
    }

    private void LevelFinished()
    {
        eventSystem.GetComponent<LevelBehaviour>().OnLevelFinished();
    }
}
