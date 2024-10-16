
指定のポイント間を、扇形の視野角でもって、徘徊し、NavMeshで移動。発見時、追尾する例。


```cs:Detect.cs
using UnityEngine;
using UnityEngine.AI;

namespace DetectSample{

    public class EnemyController_Flag : MonoBehaviour
    {
        public Transform player;        // PlayerのTransform
        public float viewRadius = 10f;  // 視野の半径
        public float viewAngle = 45f;   // 視野の角度
        public LayerMask playerMask;    // Playerのレイヤーマスク
        public LayerMask obstacleMask;  // 障害物のレイヤーマスク
        private NavMeshAgent agent;

        public Transform[] patrolPoints; // 巡回ポイント
        private Vector3 lastKnownPosition; // Playerの最後に認識した位置
        private bool isSearching = false;
        private float searchTimer = 0f;
        public float searchDuration = 5f; // 探索時間
        private int currentPatrolIndex = 0;


        private bool isResting = false; // 休憩中かどうかのフラグ
        public float restDuration = 2f; // 休憩時間
        private float restTimer = 0f;   // 休憩タイマー

        void Start()
        {
            agent = GetComponent<NavMeshAgent>();
            // agent.SetDestination(patrolPoints[currentPatrolIndex].position);
            GoToNextPatrolPoint();
        }

        void Update()
        {
            // Playerが視界に入っているか判定
            if (IsPlayerInSight())
            {
                Debug.Log("Player detected");
                // 視線の範囲を円形にし、距離を2倍に拡大
                viewRadius *= 5f;
                viewAngle = 360f;

                // Playerを追尾する
                agent.SetDestination(player.position);

                // 最後に見た位置を記憶
                lastKnownPosition = player.position;
                isSearching = true;
                searchTimer = 0f;
            }

            else if (isSearching)
            {
                Debug.Log("isSearching");
                if (Vector3.Distance(transform.position, lastKnownPosition) < agent.stoppingDistance)
                {
                    // 一定時間、周囲を探索する
                    searchTimer += Time.deltaTime;
                    if (searchTimer >= searchDuration)
                    {
                        isSearching = false;
                        // 巡回行動に戻る
                        GoToNextPatrolPoint();
                    }
                }
                else
                {
                    // 最後に見た位置に向かう
                    agent.SetDestination(lastKnownPosition);
                }
            }

    else if (!isResting && !agent.pathPending && agent.remainingDistance < agent.stoppingDistance)
    {
        // ポイントに到達したので休憩を開始
        isResting = true;
        restTimer = 0f;
    }

    else if (isResting)
    {
        // 休憩中です
        restTimer += Time.deltaTime;
        if (restTimer >= restDuration)
        {
            // 休憩を終了
            isResting = false;
            GoToNextPatrolPoint();
        }
    }

            else
            {
                // 元の視野範囲に戻す
                viewRadius = 20f;
                viewAngle = 90f;

                // 巡回行動を行う
                Patrol();
            }
        }

        bool IsPlayerInSight()
        {
            Vector3 directionToPlayer = (player.position - transform.position).normalized;
            float distanceToPlayer = Vector3.Distance(transform.position, player.position);

            // 視野内にPlayerがいるか確認
            if (distanceToPlayer < viewRadius)
            {
                // transform.forwardを使用して、ローカル座標系での前方向を基準に判定
                if (Vector3.Angle(transform.forward, directionToPlayer) < viewAngle / 2)
                {
                    // レイキャストで障害物がないか確認
                    if (!Physics.Raycast(transform.position, directionToPlayer, distanceToPlayer, obstacleMask))
                    {
                        return true;  // Playerを発見
                    }
                }
            }
            return false;  // Playerを発見していない
        }


        void Patrol()
        {
            if (!agent.pathPending && agent.remainingDistance < agent.stoppingDistance)
            {
                GoToNextPatrolPoint();
                Debug.Log("次の地点へ");
            }
        }

        void GoToNextPatrolPoint()
        {
            if (patrolPoints.Length == 0) return;

            agent.SetDestination(patrolPoints[currentPatrolIndex].position);
            currentPatrolIndex = (currentPatrolIndex + 1) % patrolPoints.Length;
}


        // 視野の可視化（デバッグ用）
        void OnDrawGizmos()
        {
            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(transform.position, viewRadius);
            Vector3 viewAngleA = DirFromAngle(-viewAngle / 2);
            Vector3 viewAngleB = DirFromAngle(viewAngle / 2);
            Gizmos.DrawLine(transform.position, transform.position + viewAngleA * viewRadius);
            Gizmos.DrawLine(transform.position, transform.position + viewAngleB * viewRadius);
        }

        Vector3 DirFromAngle(float angleInDegrees)
        {
            // オブジェクトのローカル座標系での前方向を基準にする
            return transform.forward * Mathf.Cos(angleInDegrees * Mathf.Deg2Rad) + 
                transform.right * Mathf.Sin(angleInDegrees * Mathf.Deg2Rad);
        }

    }
}
```

<br>

---
---

<br>

上記内容をステートパターンを使用して書いてみた

+ EnemyController_State.cs
+ State.cs

Stateを継承した実際の行動に関するプログラム
+ SearchState.cs
+ ChaseState.cs
+ PatrolState.cs
+ RestState.cs


```cs:EnemyController_State.cs
using UnityEngine;
using UnityEngine.AI;

namespace DetectSample
{
    public class EnemyController_State : MonoBehaviour
    {
        public Transform player;
        public float viewRadius = 10f;
        public float viewAngle = 45f;
        public LayerMask playerMask;
        public LayerMask obstacleMask{ get; set; }
        public NavMeshAgent agent;

        public Transform[] patrolPoints;
        public float searchDuration = 5f;
        public float restDuration = 2f;

        public Vector3 lastKnownPosition { get; set; }
        public bool isSearching { get; set; } = false;
        public float searchTimer { get; set; } = 0f;
        public bool isResting { get; set; } = false;
        public float restTimer { get; set; } = 0f;

        private State currentState;

        void Start()
        {
            agent = GetComponent<NavMeshAgent>();
            ChangeState(new PatrolState(this));
        }

        void Update()
        {
            currentState.UpdateState();
        }

        public void ChangeState(State newState)
        {
            if (currentState != null)
            {
                currentState.ExitState();
            }
            currentState = newState;
            currentState.EnterState();
        }

        public bool IsPlayerInSight()
        {
            Vector3 directionToPlayer = (player.position - transform.position).normalized;
            float distanceToPlayer = Vector3.Distance(transform.position, player.position);

            if (distanceToPlayer < viewRadius)
            {
                if (Vector3.Angle(transform.forward, directionToPlayer) < viewAngle / 2)
                {
                    if (!Physics.Raycast(transform.position, directionToPlayer, distanceToPlayer, obstacleMask))
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        public void SetDestination(Vector3 destination)
        {
            agent.SetDestination(destination);
        }

        public bool IsAtDestination()
        {
            return !agent.pathPending && agent.remainingDistance < agent.stoppingDistance;
        }

        public void ResetVision()
        {
            viewRadius = 10f;
            viewAngle = 45f;
        }
    }
}

```

```cs:State.cs
namespace DetectSample
{
    public abstract class State
    {
        public abstract void EnterState();
        public abstract void UpdateState();
        public virtual void ExitState() { } // ExitState メソッドを追加
    }
}

```


```cs:SearchState.cs
using UnityEngine;

namespace DetectSample
{
    public class SearchState : State
    {
        private EnemyController_State enemy;

        public SearchState(EnemyController_State enemy)
        {
            this.enemy = enemy;
        }

        public override void EnterState()
        {
            enemy.searchTimer = 0f;
            enemy.SetDestination(enemy.lastKnownPosition);
        }

        public override void UpdateState()
        {
            if (Vector3.Distance(enemy.transform.position, enemy.lastKnownPosition) < enemy.agent.stoppingDistance)
            {
                enemy.searchTimer += Time.deltaTime;
                if (enemy.searchTimer >= enemy.searchDuration)
                {
                    enemy.ChangeState(new PatrolState(enemy));
                }
            }
            else
            {
                enemy.SetDestination(enemy.lastKnownPosition);
            }
        }

        public override void ExitState()
        {
            // 探索中のフラグとタイマーをリセット
            enemy.isSearching = false;
            enemy.searchTimer = 0f;
        }
    }
}

```


```cs:ChaseState.cs
using UnityEngine;

namespace DetectSample
{
    public class ChaseState : State
    {
        private EnemyController_State enemy;

        public ChaseState(EnemyController_State enemy)
        {
            this.enemy = enemy;
        }

        public override void EnterState()
        {
            enemy.viewRadius *= 5f;
            enemy.viewAngle = 360f;
        }

        public override void UpdateState()
        {
            if (enemy.IsPlayerInSight())
            {
                enemy.SetDestination(enemy.player.position);
                enemy.lastKnownPosition = enemy.player.position;
            }
            else
            {
                enemy.ChangeState(new SearchState(enemy));
            }
        }

        public override void ExitState()
        {
            // 視野範囲を元に戻す
            enemy.ResetVision();
        }
    }
}

```


```cs:PatrolState.cs
using UnityEngine;

namespace DetectSample
{
    public class PatrolState : State
    {
        private EnemyController_State enemy;
        private int currentPatrolIndex = 0;

        public PatrolState(EnemyController_State enemy)
        {
            this.enemy = enemy;
        }

        public override void EnterState()
        {
            GoToNextPatrolPoint();
        }

        public override void UpdateState()
        {
            if (enemy.isResting)
            {
                enemy.restTimer += Time.deltaTime;
                if (enemy.restTimer >= enemy.restDuration)
                {
                    enemy.isResting = false;
                    GoToNextPatrolPoint();
                }
            }
            else if (enemy.IsAtDestination())
            {
                enemy.isResting = true;
                enemy.restTimer = 0f;
            }
        }

        public override void ExitState()
        {
            // 休憩中のフラグとタイマーをリセット
            enemy.isResting = false;
            enemy.restTimer = 0f;
        }

        private void GoToNextPatrolPoint()
        {
            if (enemy.patrolPoints.Length == 0) return;

            enemy.SetDestination(enemy.patrolPoints[currentPatrolIndex].position);
            currentPatrolIndex = (currentPatrolIndex + 1) % enemy.patrolPoints.Length;
        }
    }
}

```


```cs:RestState.cs
using UnityEngine;

namespace DetectSample
{
    public class RestState : State
    {
        private EnemyController_State enemy;

        public RestState(EnemyController_State enemy)
        {
            this.enemy = enemy;
        }

        public override void EnterState()
        {
            enemy.restTimer = 0f;
        }

        public override void UpdateState()
        {
            enemy.restTimer += Time.deltaTime;
            if (enemy.restTimer >= enemy.restDuration)
            {
                enemy.ChangeState(new PatrolState(enemy));
            }
        }

        public override void ExitState()
        {
            // 休憩中のフラグとタイマーをリセット
            enemy.isResting = false;
            enemy.restTimer = 0f;
        }
    }
}

```