# 31-4: Heartbeat TTL env default + sidecar self-suicide test

## 작업

- `wily.py`의 `command_live_heartbeat` 또는 사이드카 진입점에서 `--ttl`이 명시되지 않으면 환경변수 `WILY_BOARD_HEARTBEAT_TTL_SECONDS` 값을 사용
- 환경변수도 없으면 default `14400` (4시간)
- 시작 시각 + TTL을 사이드카 메모리에 저장, 매 tick마다 비교
- TTL 만료 시: `released` event emit + `.alive` 파일 제거 + 정상 exit

## 회귀 테스트

```python
def test_heartbeat_sidecar_ttl_self_suicide(tmp_path, monkeypatch):
    # WILY_BOARD_HEARTBEAT_TTL_SECONDS=2, no --ttl arg
    # spawn sidecar, wait ~3s, assert process exited + released event recorded
```

## 검증

- TTL 2초로 띄운 사이드카가 ~3초 후 자살
- TTL 만료 시 마지막 이벤트가 `released`인지 확인 (intermediate `heartbeat`이 아님)
- `--ttl 60`이 env보다 우선 적용되는지
