# unstable_addTransitionType - This feature is available in the latest Experimental version of React

URL: https://ko.react.dev/reference/react/addTransitionType

API 참고서
API
unstable_addTransitionType
- This feature is available in the latest Experimental version of React
Experimental Feature
This API is experimental and is not available in a stable version of React yet.
You can try it by upgrading React packages to the most recent experimental version:
react@experimental
react-dom@experimental
eslint-plugin-react-hooks@experimental
Experimental versions of React may contain bugs. Don’t use them in production.
unstable_addTransitionType
lets you specify the cause of a transition.
```
startTransition(() => {  unstable_addTransitionType('my-transition-type');  setState(newState);});
```
Reference
addTransitionType
Usage
Adding the cause of a transition
Customize animations using browser view transition types
Customize animations using
View Transition
Class
Customize animations using
ViewTransition
events
Troubleshooting
TODO
Reference
addTransitionType
Parameters
type
: The type of transition to add. This can be any string.
Returns
startTransition
does not return anything.
Caveats
If multiple transitions are combined, all Transition Types are collected. You can also add more than one type to a Transition.
Transition Types are reset after each commit. This means a
<Suspense>
fallback will associate the types after a
startTransition
, but revealing the content does not.
Usage
Adding the cause of a transition
Call
addTransitionType
inside of
startTransition
to indicate the cause of a transition:
```
import { startTransition, unstable_addTransitionType } from 'react';function Submit({action) {  function handleClick() {    startTransition(() => {      unstable_addTransitionType('submit-click');      action();    });  }  return
Click me
;}
```
When you call
addTransitionType
inside the scope of
startTransition
, React will associate
submit-click
as one of the causes for the Transition.
Currently, Transition Types can be used to customize different animations based on what caused the Transition. You have three different ways to choose from for how to use them:
Customize animations using browser view transition types
Customize animations using
View Transition
Class
Customize animations using
ViewTransition
events
In the future, we plan to support more use cases for using the cause of a transition.
Customize animations using browser view transition types
When a
ViewTransition
activates from a transition, React adds all the Transition Types as browser
view transition types
to the element.
This allows you to customize different animations based on CSS scopes:
```
function Component() {  return (
Hello
);}startTransition(() => {  unstable_addTransitionType('my-transition-type');  setShow(true);});
```
```
:root:active-view-transition-type(my-transition-type) {  &::view-transition-...(...) {    ...  }}
```
Customize animations using
View Transition
Class
You can customize animations for an activated
ViewTransition
based on type by passing an object to the View Transition Class:
```
function Component() {  return (
Hello
);}// ...startTransition(() => {  unstable_addTransitionType('my-transition-type');  setState(newState);});
```
If multiple types match, then they’re joined together. If no types match then the special “default” entry is used instead. If any type has the value “none” then that wins and the ViewTransition is disabled (not assigned a name).
These can be combined with enter/exit/update/layout/share props to match based on kind of trigger and Transition Type.
```
```
Customize animations using
ViewTransition
events
You can imperatively customize animations for an activated
ViewTransition
based on type using View Transition events:
```
{  if (types.includes('navigation-back')) {    ...  } else if (types.includes('navigation-forward')) {    ...  } else {    ...  }}}>
```
This allows you to pick different imperative Animations based on the cause.
Troubleshooting
TODO
이전
experimental_taintUniqueValue
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