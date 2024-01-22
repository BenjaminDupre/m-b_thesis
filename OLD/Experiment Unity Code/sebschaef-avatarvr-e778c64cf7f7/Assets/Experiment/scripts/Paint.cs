using System.Collections;
using System.Collections.Generic;
using UnityDLL.Haptic;
using UnityEngine;

public class Paint : MonoBehaviour
{
    public Texture2D texture;
    public LayerMask layer;
    public LayerMask layerSupport;
    public float radius;
    public int brushSize;
    public float intensity;
    public Color[] initialColors;
    private ActuatorInfo actuatorInfo;
    private RaycastHit hit;

    // Use this for initialization
    void Start()
    {
        actuatorInfo = GetComponentInParent<ActuatorInfo>();

        for (int x = 0; x < texture.width; x++)
        {
            for (int y = 0; y < texture.height; y++)
            {
                texture.SetPixel(x, y, Color.white);
            }
        }
        initialColors = texture.GetPixels();
        texture.Apply();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        texture.Apply();

        if (brushSize <= 0)
            brushSize = 1;

        Collider[] cols = Physics.OverlapSphere(this.transform.position, radius, layerSupport);

        if (cols != null && cols.Length != 0)
        {
            Vector3 rayOrigin = cols[0].ClosestPoint(transform.position) + cols[0].transform.up;

            Debug.DrawRay(rayOrigin, -cols[0].transform.up, Color.magenta);

            if (Physics.Raycast(rayOrigin, -cols[0].transform.up, out hit, Mathf.Infinity, layer))
            {
                Vector3 pixelUV = hit.textureCoord;

                Debug.Log(hit.collider.name + ", " + hit.textureCoord + ", " + hit.point);

                pixelUV.x *= texture.width;
                pixelUV.y *= texture.height;

                for (int i = -brushSize; i <= brushSize; i++)
                {
                    if ((int)pixelUV.x + i >= 0 && (int)pixelUV.x + i <= texture.width - 1)
                    {
                        texture.SetPixel((int)pixelUV.x + i, (int)pixelUV.y, Color.black);
                        for (int j = -brushSize; j <= brushSize; j++)
                        {
                            if ((int)pixelUV.y + j >= 0 && (int)pixelUV.y + j <= texture.height - 1)
                            {
                                texture.SetPixel((int)pixelUV.x + i, (int)pixelUV.y + j, Color.black);
                            }
                        }
                    }
                }

                //HapticSystem.PlayPulse(intensity, 100, actuatorInfo.location, actuatorInfo.userIndex, actuatorInfo.actuator);
                texture.Apply();
            }
        }
    }
}
