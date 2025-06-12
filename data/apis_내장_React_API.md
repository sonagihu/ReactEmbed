# 내장 React API

URL: https://ko.react.dev/reference/react/apis

API 참고서
내장 React API
Hook
과
컴포넌트
외에도
react
패키지는 컴포넌트를 정의하는데 유용한 몇 가지 API를 가지고 있습니다. 이 페이지는 최신 React API를 모두 나열합니다.
act
lets you wrap renders and interactions in tests to ensure updates have processed before making assertions.
cache
를 통해 가져온 데이터나 연산의 결과를 캐싱합니다.
createContext
lets you define and provide context to the child components. Used with
useContext
.
lazy
lets you defer loading a component’s code until it’s rendered for the first time.
memo
lets your component skip re-renders with same props. Used with
useMemo
and
useCallback
.
startTransition
lets you mark a state update as non-urgent. Similar to
useTransition
.
use
는 Promise나 Context와 같은 데이터를 참조하는 React Hook입니다.
Resource APIs
Resource
를 State의 일부로 포함하지 않고도 컴포넌트에서 Resource에 액세스할 수 있습니다. 예를 들어, 컴포넌트는 Promise에서 메시지를 읽거나 Context에서 스타일 정보를 읽을 수 있습니다.
Resource에서 값을 읽으려면 다음 API를 사용하세요.
use
를 사용하면
Promise
나
Context
와 같은 Resource의 값을 읽을 수 있습니다.
```
function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...}
```
이전
<ViewTransition>
다음
act
Copyright © Meta Platforms, Inc
no uwu plz
uwu?
Logo by
@sawaratsuki1004
React 학습하기
빠르게 시작하기
설치하기
UI 표현하기
상호작용성 더하기
State 관리하기
탈출구
API 참고서
React APIs
React DOM APIs
커뮤니티
행동 강령
팀 소개
문서 기여자
감사의 말
더 보기
블로그
React Native
개인 정보 보호
약관