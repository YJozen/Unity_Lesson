using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NuiiAllowTypeTest : MonoBehaviour
{
    public Vector2? a;

    void Start()
    {
        if (a.HasValue)
        {
            // a が null でない場合にのみ処理を行う
            Vector2 value = a.Value;
            
            // Absolute value の計算
            Vector2 absValue = new Vector2(Mathf.Abs(value.x), Mathf.Abs(value.y));
            Debug.Log("Absolute Vector2: " + absValue);

            // Magnitude の計算
            float magnitude = value.magnitude;
            Debug.Log("Magnitude: " + magnitude);
        }
        else
        {
            Debug.Log("a is null.");
        }
    }
}