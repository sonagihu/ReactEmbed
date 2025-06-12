# <ViewTransition> - This feature is available in the latest Experimental version of React

URL: https://ko.react.dev/reference/react/ViewTransition

API 참고서
컴포넌트
<ViewTransition>
- This feature is available in the latest Experimental version of React
Experimental Feature
This API is experimental and is not available in a stable version of React yet.
You can try it by upgrading React packages to the most recent experimental version:
react@experimental
react-dom@experimental
eslint-plugin-react-hooks@experimental
Experimental versions of React may contain bugs. Don’t use them in production.
<ViewTransition>
lets you animate elements that update inside a Transition.
```
import {unstable_ViewTransition as ViewTransition} from 'react';
...
```
Reference
<ViewTransition>
View Transition Class
Styling View Transitions
Usage
Animating an element on enter/exit
Animating a shared element
Animating reorder of items in a list
Animating from Suspense content
Opting-out of an animation
Customizing animations
Customizing animations with types
Building View Transition enabled routers
Troubleshooting
My
<ViewTransition>
is not activating
I’m getting an error “There are two
<ViewTransition name=%s>
components with the same name mounted at the same time.”
Reference
<ViewTransition>
Wrap elements in
<ViewTransition>
to animate them when they update inside a
Transition
. React uses the following heuristics to determine if a View Transition activates for an animation:
enter
: If a
ViewTransition
itself gets inserted in this Transition, then this will activate.
exit
: If a
ViewTransition
itself gets deleted in this Transition, then this will activate.
update
: If a
ViewTransition
has any DOM mutations inside it that React is doing (such as a prop changing) or if the
ViewTransition
boundary itself changes size or position due to an immediate sibling. If there are nested
ViewTransition
then the mutation applies to them and not the parent.
share
: If a named
ViewTransition
is inside a deleted subtree and another named
ViewTransition
with the same name is part of an inserted subtree in the same Transition, they form a Shared Element Transition, and it animates from the deleted one to the inserted one.
By default,
<ViewTransition>
animates with a smooth cross-fade (the browser default view transition). You can customize the animation by providing a
View Transition Class
to the
<ViewTransition>
component. You can customize animations for each kind of trigger (see
Styling View Transitions
).
자세히 살펴보기
How does
<ViewTransition>
work?
자세히 보기
Under the hood, React applies
view-transition-name
to inline styles of the nearest DOM node nested inside the
<ViewTransition>
component. If there are multiple sibling DOM nodes like
<ViewTransition><div /><div /></ViewTransition>
then React adds a suffix to the name to make each unique but conceptually they’re part of the same one. React doesn’t apply these eagerly but only at the time that boundary should participate in an animation.
React automatically calls
startViewTransition
itself behind the scenes so you should never do that yourself. In fact, if you have something else on the page running a ViewTransition React will interrupt it. So it’s recommended that you use React itself to coordinate these. If you had other ways of trigger ViewTransitions in the past, we recommend that you migrate to the built-in way.
If there are other React ViewTransitions already running then React will wait for them to finish before starting the next one. However, importantly if there are multiple updates happening while the first one is running, those will all be batched into one. If you start A->B. Then in the meantime you get an update to go to C and then D. When the first A->B animation finishes the next one will animate from B->D.
The
getSnapshotBeforeUpdate
life-cycle will be called before
startViewTransition
and some
view-transition-name
will update at the same time.
Then React calls
startViewTransition
. Inside the
updateCallback
, React will:
Apply its mutations to the DOM and invoke useInsertionEffects.
Wait for fonts to load.
Call componentDidMount, componentDidUpdate, useLayoutEffect and refs.
Wait for any pending Navigation to finish.
Then React will measure any changes to the layout to see which boundaries will need to animate.
After the ready Promise of the
startViewTransition
is resolved, React will then revert the
view-transition-name
. Then React will invoke the
onEnter
,
onExit
,
onUpdate
and
onShare
callbacks to allow for manual programmatic control over the Animations. This will be after the built-in default ones have already been computed.
If a
flushSync
happens to get in the middle of this sequence, then React will skip the Transition since it relies on being able to complete synchronously.
After the finished Promise of the
startViewTransition
is resolved, React will then invoke
useEffect
. This prevents those from interfering with the performance of the Animation. However, this is not a guarantee because if another
setState
happens while the Animation is running it’ll still have to invoke the
useEffect
earlier to preserve the sequential guarantees.
Props
By default,
<ViewTransition>
animates with a smooth cross-fade. You can customize the animation, or specify a shared element transition, with these props:
optional
enter
: A string or object. The
View Transition Class
to apply when enter is activated.
optional
exit
: A string or object. The
View Transition Class
to apply when exit is activated.
optional
update
: A string or object. The
View Transition Class
to apply when an update is activated.
optional
share
: A string or object. The
View Transition Class
to apply when a shared element is activated.
optional
default
: A string or object. The
View Transition Class
used when no other matching activation prop is found.
optional
name
: A string or object. The name of the View Transition used for shared element transitions. If not provided, React will use a unique name for each View Transition to prevent unexpected animations.
Callback
These callbacks allow you to adjust the animation imperatively using the
animate
APIs:
optional
onEnter
: A function. React calls
onEnter
after an “enter” animation.
optional
onExit
: A function. React calls
onExit
after an “exit” animation.
optional
onShare
: A function. React calls
onShare
after a “share” animation.
optional
onUpdate
: A function. React calls
onUpdate
after an “update” animation.
Each callback receives as arguments:
element
: The DOM element that was animated.
types
: The
Transition Types
included in the animation.
View Transition Class
The View Transition Class is the CSS class name(s) applied by React during the transition when the ViewTransition activates. It can be a string or an object.
string
: the
class
added on the child elements when activated. If
'none'
is provided, no class will be added.
object
: the class added on the child elements will be the key matching View Transition type added with
addTransitionType
. The object can also specify a
default
to use if no matching type is found.
The value
'none'
can be used to prevent a View Transition from activating for a specific trigger.
Styling View Transitions
중요합니다!
In many early examples of View Transitions around the web, you’ll have seen using a
view-transition-name
and then style it using
::view-transition-...(my-name)
selectors. We don’t recommend that for styling. Instead, we normally recommend using a View Transition Class instead.
To customize the animation for a
<ViewTransition>
you can provide a View Transition Class to one of the activation props. The View Transition Class is a CSS class name that React applies to the child elements when the ViewTransition activates.
For example, to customize an “enter” animation, provide a class name to the
enter
prop:
```
```
When the
<ViewTransition>
activates an “enter” animation, React will add the class name
slide-in
. Then you can refer to this class using
view transition pseudo selectors
to build reusable animations:
```
::view-transition-group(.slide-in) {  }::view-transition-old(.slide-in) {}::view-transition-new(.slide-in) {}
```
In the future, CSS libraries may add built-in animations using View Transition Classes to make this easier to use.
Caveats
By default,
setState
updates immediately and does not activate
<ViewTransition>
, only updates wrapped in a
Transition
. You can also use
<Suspense>
to opt-in to a Transition to
reveal content
.
<ViewTransition>
creates an image that can be moved around, scaled and cross-faded. Unlike Layout Animations you may have seen in React Native or Motion, this means that not every individual Element inside of it animates its position. This can lead to better performance and a more continuous feeling, smooth animation compared to animating every individual piece. However, it can also lose continuity in things that should be moving by themselves. So you might have to add more
<ViewTransition>
boundaries manually as a result.
Many users may prefer not having animations on the page. React doesn’t automatically disable animations for this case. We recommend that using the
@media (prefers-reduced-motion)
media query to disable animations or tone them down based on user preference. In the future, CSS libraries may have this built-in to their presets.
Currently,
<ViewTransition>
only works in the DOM. We’re working on adding support for React Native and other platforms.
Usage
Animating an element on enter/exit
Enter/Exit Transitions trigger when a
<ViewTransition>
is added or removed by a component in a transition:
```
function Child() {  return
Hi
}function Parent() {  const [show, setShow] = useState();  if (show) {    return
;  }  return null;}
```
When
setShow
is called,
show
switches to
true
and the
Child
component is rendered. When
setShow
is called inside
startTransition
, and
Child
renders a
ViewTransition
before any other DOM nodes, an
enter
animation is triggered.
When
show
switches back to
false
, an
exit
animation is triggered.
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
}
from
'react'
;
import
{
Video
}
from
"./Video"
;
import
videos
from
"./data"
function
Item
(
)
{
return
(
<
ViewTransition
>
<
Video
video
=
{
videos
[
0
]
}
/>
</
ViewTransition
>
)
;
}
export
default
function
Component
(
)
{
const
[
showItem
,
setShowItem
]
=
useState
(
false
)
;
return
(
<
>
<
button
onClick
=
{
(
)
=>
{
startTransition
(
(
)
=>
{
setShowItem
(
(
prev
)
=>
!
prev
)
;
}
)
;
}
}
>
{
showItem
?
'➖'
:
'➕'
}
</
button
>
{
showItem
?
<
Item
/>
:
null
}
</
>
)
;
}
자세히 보기
주의하세요!
<ViewTransition>
only activates if it is placed before any DOM node. If
Child
instead looked like this, no animation would trigger:
```
function Component() {  return (
Hi
);}
```
Animating a shared element
Normally, we don’t recommend assigning a name to a
<ViewTransition>
and instead let React assign it an automatic name. The reason you might want to assign a name is to animate between completely different components when one tree unmounts and another tree mounts at the same time. To preserve continuity.
```
```
When one tree unmounts and another mounts, if there’s a pair where the same name exists in the unmounting tree and the mounting tree, they trigger the “share” animation on both. It animates from the unmounting side to the mounting side.
Unlike an exit/enter animation this can be deeply inside the deleted/mounted tree. If a
<ViewTransition>
would also be eligible for exit/enter, then the “share” animation takes precedence.
If Transition first unmounts one side and then leads to a
<Suspense>
fallback being shown before eventually the new name being mounted, then no shared element transition happens.
App.js
Video.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
}
from
"react"
;
import
{
Video
,
Thumbnail
,
FullscreenVideo
}
from
"./Video"
;
import
videos
from
"./data"
;
export
default
function
Component
(
)
{
const
[
fullscreen
,
setFullscreen
]
=
useState
(
false
)
;
if
(
fullscreen
)
{
return
<
FullscreenVideo
video
=
{
videos
[
0
]
}
onExit
=
{
(
)
=>
startTransition
(
(
)
=>
setFullscreen
(
false
)
)
}
/>
}
return
<
Video
video
=
{
videos
[
0
]
}
onClick
=
{
(
)
=>
startTransition
(
(
)
=>
setFullscreen
(
true
)
)
}
/>
}
자세히 보기
중요합니다!
If either the mounted or unmounted side of a pair is outside the viewport, then no pair is formed. This ensures that it doesn’t fly in or out of the viewport when something is scrolled. Instead it’s treated as a regular enter/exit by itself.
This does not happen if the same Component instance changes position, which triggers an “update”. Those animate regardless if one position is outside the viewport.
There’s currently a quirk where if a deeply nested unmounted
<ViewTransition>
is inside the viewport but the mounted side is not within the viewport, then the unmounted side animates as its own “exit” animation even if it’s deeply nested instead of as part of the parent animation.
주의하세요!
It’s important that there’s only one thing with the same name mounted at a time in the entire app. Therefore it’s important to use unique namespaces for the name to avoid conflicts. To ensure you can do this you might want to add a constant in a separate module that you import.
```
export const MY_NAME = "my-globally-unique-name";import {MY_NAME} from './shared-name';...
```
Animating reorder of items in a list
```
items.map(item =>
)
```
When reordering a list, without updating the content, the “update” animation triggers on each
<ViewTransition>
in the list if they’re outside a DOM node. Similar to enter/exit animations.
This means that this will trigger the animation on this
<ViewTransition>
:
```
function Component() {  return
...
;}
```
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
}
from
"react"
;
import
{
Video
}
from
"./Video"
;
import
videos
from
"./data"
;
export
default
function
Component
(
)
{
const
[
orderedVideos
,
setOrderedVideos
]
=
useState
(
videos
)
;
const
reorder
=
(
)
=>
{
startTransition
(
(
)
=>
{
setOrderedVideos
(
(
prev
)
=>
{
return
[
...
prev
.
sort
(
(
)
=>
Math
.
random
(
)
-
0.5
)
]
;
}
)
;
}
)
;
}
;
return
(
<
>
<
button
onClick
=
{
reorder
}
>
🎲
</
button
>
<
div
className
=
"listContainer"
>
{
orderedVideos
.
map
(
(
video
,
i
)
=>
{
return
(
<
ViewTransition
key
=
{
video
.
title
}
>
<
Video
video
=
{
video
}
/>
</
ViewTransition
>
)
;
}
)
}
</
div
>
</
>
)
;
}
자세히 보기
However, this wouldn’t animate each individual item:
```
function Component() {  return
...
;}
```
Instead, any parent
<ViewTransition>
would cross-fade. If there is no parent
<ViewTransition>
then there’s no animation in that case.
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
}
from
"react"
;
import
{
Video
}
from
"./Video"
;
import
videos
from
"./data"
;
export
default
function
Component
(
)
{
const
[
orderedVideos
,
setOrderedVideos
]
=
useState
(
videos
)
;
const
reorder
=
(
)
=>
{
startTransition
(
(
)
=>
{
setOrderedVideos
(
(
prev
)
=>
{
return
[
...
prev
.
sort
(
(
)
=>
Math
.
random
(
)
-
0.5
)
]
;
}
)
;
}
)
;
}
;
return
(
<
>
<
button
onClick
=
{
reorder
}
>
🎲
</
button
>
<
ViewTransition
>
<
div
className
=
"listContainer"
>
{
orderedVideos
.
map
(
(
video
,
i
)
=>
{
return
<
Video
video
=
{
video
}
key
=
{
video
.
title
}
/>
;
}
)
}
</
div
>
</
ViewTransition
>
</
>
)
;
}
자세히 보기
This means you might want to avoid wrapper elements in lists where you want to allow the Component to control its own reorder animation:
```
items.map(item =>
)
```
The above rule also applies if one of the items updates to resize, which then causes the siblings to resize, it’ll also animate its sibling
<ViewTransition>
but only if they’re immediate siblings.
This means that during an update, which causes a lot of re-layout, it doesn’t individually animate every
<ViewTransition>
on the page. That would lead to a lot of noisy animations which distracts from the actual change. Therefore React is more conservative about when an individual animation triggers.
주의하세요!
It’s important to properly use keys to preserve identity when reordering lists. It might seem like you could use “name”, shared element transitions, to animate reorders but that would not trigger if one side was outside the viewport. To animate a reorder you often want to show that it went to a position outside the viewport.
Animating from Suspense content
Just like any Transition, React waits for data and new CSS (
<link rel="stylesheet" precedence="...">
) before running the animation. In addition to this, ViewTransitions also wait up to 500ms for new fonts to load before starting the animation to avoid them flickering in later. For the same reason, an image wrapped in ViewTransition will wait for the image to load.
If it’s inside a new Suspense boundary instance, then the fallback is shown first. After the Suspense boundary fully loads, it triggers the
<ViewTransition>
to animate the reveal to the content.
Currently, this only happens for client-side Transition. In the future, this will also animate Suspense boundary for streaming SSR when content from the server suspends during the initial load.
There are two ways to animate Suspense boundaries depending on where you place the
<ViewTransition>
:
Update:
```
}>
```
In this scenario when the content goes from A to B, it’ll be treated as an “update” and apply that class if appropriate. Both A and B will get the same view-transition-name and therefore they’re acting as a cross-fade by default.
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
,
Suspense
}
from
'react'
;
import
{
Video
,
VideoPlaceholder
}
from
"./Video"
;
import
{
useLazyVideoData
}
from
"./data"
function
LazyVideo
(
)
{
const
video
=
useLazyVideoData
(
)
;
return
(
<
Video
video
=
{
video
}
/>
)
;
}
export
default
function
Component
(
)
{
const
[
showItem
,
setShowItem
]
=
useState
(
false
)
;
return
(
<
>
<
button
onClick
=
{
(
)
=>
{
startTransition
(
(
)
=>
{
setShowItem
(
(
prev
)
=>
!
prev
)
;
}
)
;
}
}
>
{
showItem
?
'➖'
:
'➕'
}
</
button
>
{
showItem
?
(
<
ViewTransition
>
<
Suspense
fallback
=
{
<
VideoPlaceholder
/>
}
>
<
LazyVideo
/>
</
Suspense
>
</
ViewTransition
>
)
:
null
}
</
>
)
;
}
자세히 보기
Enter/Exit:
```
}>
```
In this scenario, these are two separate ViewTransition instances each with their own
view-transition-name
. This will be treated as an “exit” of the
<A>
and an “enter” of the
<B>
.
You can achieve different effects depending on where you choose to place the
<ViewTransition>
boundary.
Opting-out of an animation
Sometimes you’re wrapping a large existing component, like a whole page, and you want to animate some updates, such as changing the theme. However, you don’t want it to opt-in all updates inside the whole page to cross-fade when they’re updating. Especially if you’re incrementally adding more animations.
You can use the class “none” to opt-out of an animation. By wrapping your children in a “none” you can disable animations for updates to them while the parent still triggers.
```
{children}
```
This will only animate if the theme changes and not if only the children update. The children can still opt-in again with their own
<ViewTransition>
but at least it’s manual again.
Customizing animations
By default,
<ViewTransition>
includes the default cross-fade from the browser.
To customize animations, you can provide props to the
<ViewTransition>
component to specify which animations to use, based on how the
<ViewTransition>
activates.
For example, we can slow down the default cross fade animation:
```
```
And define slow-fade in CSS using view transition classes:
```
::view-transition-old(.slow-fade) {    animation-duration: 500ms;}::view-transition-new(.slow-fade) {    animation-duration: 500ms;}
```
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
}
from
'react'
;
import
{
Video
}
from
"./Video"
;
import
videos
from
"./data"
function
Item
(
)
{
return
(
<
ViewTransition
default
=
"slow-fade"
>
<
Video
video
=
{
videos
[
0
]
}
/>
</
ViewTransition
>
)
;
}
export
default
function
Component
(
)
{
const
[
showItem
,
setShowItem
]
=
useState
(
false
)
;
return
(
<
>
<
button
onClick
=
{
(
)
=>
{
startTransition
(
(
)
=>
{
setShowItem
(
(
prev
)
=>
!
prev
)
;
}
)
;
}
}
>
{
showItem
?
'➖'
:
'➕'
}
</
button
>
{
showItem
?
<
Item
/>
:
null
}
</
>
)
;
}
자세히 보기
In addition to setting the
default
, you can also provide configurations for
enter
,
exit
,
update
, and
share
animations.
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
useState
,
startTransition
}
from
'react'
;
import
{
Video
}
from
"./Video"
;
import
videos
from
"./data"
function
Item
(
)
{
return
(
<
ViewTransition
enter
=
"slide-in"
exit
=
"slide-out"
>
<
Video
video
=
{
videos
[
0
]
}
/>
</
ViewTransition
>
)
;
}
export
default
function
Component
(
)
{
const
[
showItem
,
setShowItem
]
=
useState
(
false
)
;
return
(
<
>
<
button
onClick
=
{
(
)
=>
{
startTransition
(
(
)
=>
{
setShowItem
(
(
prev
)
=>
!
prev
)
;
}
)
;
}
}
>
{
showItem
?
'➖'
:
'➕'
}
</
button
>
{
showItem
?
<
Item
/>
:
null
}
</
>
)
;
}
자세히 보기
Customizing animations with types
You can use the
addTransitionType
API to add a class name to the child elements when a specific transition type is activated for a specific activation trigger. This allows you to customize the animation for each type of transition.
For example, to customize the animation for all forward and backward navigations:
```
...
// in your router:startTransition(() => {  addTransitionType('navigation-' + navigationType);});
```
When the ViewTransition activates a “navigation-back” animation, React will add the class name “slide-right”. When the ViewTransition activates a “navigation-forward” animation, React will add the class name “slide-left”.
In the future, routers and other libraries may add support for standard view-transition types and styles.
App.js
App.js
초기화
포크
import
{
unstable_ViewTransition
as
ViewTransition
,
unstable_addTransitionType
as
addTransitionType
,
useState
,
startTransition
,
}
from
"react"
;
import
{
Video
}
from
"./Video"
;
import
videos
from
"./data"
function
Item
(
)
{
return
(
<
ViewTransition
enter
=
{
{
"add-video-back"
:
"slide-in-back"
,
"add-video-forward"
:
"slide-in-forward"
}
}
exit
=
{
{
"remove-video-back"
:
"slide-in-forward"
,
"remove-video-forward"
:
"slide-in-back"
}
}
>
<
Video
video
=
{
videos
[
0
]
}
/>
</
ViewTransition
>
)
;
}
export
default
function
Component
(
)
{
const
[
showItem
,
setShowItem
]
=
useState
(
false
)
;
return
(
<
>
<
div
className
=
"button-container"
>
<
button
onClick
=
{
(
)
=>
{
startTransition
(
(
)
=>
{
if
(
showItem
)
{
addTransitionType
(
"remove-video-back"
)
}
else
{
addTransitionType
(
"add-video-back"
)
}
setShowItem
(
(
prev
)
=>
!
prev
)
;
}
)
;
}
}
>
⬅️
</
button
>
<
button
onClick
=
{
(
)
=>
{
startTransition
(
(
)
=>
{
if
(
showItem
)
{
addTransitionType
(
"remove-video-forward"
)
}
else
{
addTransitionType
(
"add-video-forward"
)
}
setShowItem
(
(
prev
)
=>
!
prev
)
;
}
)
;
}
}
>
➡️
</
button
>
</
div
>
{
showItem
?
<
Item
/>
:
null
}
</
>
)
;
}
자세히 보기
Building View Transition enabled routers
React waits for any pending Navigation to finish to ensure that scroll restoration happens within the animation. If the Navigation is blocked on React, your router must unblock in
useLayoutEffect
since
useEffect
would lead to a deadlock.
If a
startTransition
is started from the legacy popstate event, such as during a “back”-navigation then it must finish synchronously to ensure scroll and form restoration works correctly. This is in conflict with running a View Transition animation. Therefore, React will skip animations from popstate. Therefore animations won’t run for the back button. You can fix this by upgrading your router to use the Navigation API.
Troubleshooting
My
<ViewTransition>
is not activating
<ViewTransition>
only activates if it is placed is before any DOM node:
```
function Component() {  return (
Hi
);}
```
To fix, ensure that the
<ViewTransition>
comes before any other DOM nodes:
```
function Component() {  return (
Hi
);}
```
I’m getting an error “There are two
<ViewTransition name=%s>
components with the same name mounted at the same time.”
This error occurs when two
<ViewTransition>
components with the same
name
are mounted at the same time:
```
function Item() {  // 🚩 All items will get the same "name".  return
...
;}function ItemList({items}) {  return (    <>      {item.map(item =>
)}      );}
```
This will cause the View Transition to error. In development, React detects this issue to surface it and logs two errors:
Console
There are two
<ViewTransition name=%s>
components with the same name mounted at the same time. This is not supported and will cause View Transitions to error. Try to use a more unique name e.g. by using a namespace prefix and adding the id of an item to the name.
at Item
at ItemList
The existing
<ViewTransition name=%s>
duplicate has this stack trace.
at Item
at ItemList
To fix, ensure that there’s only one
<ViewTransition>
with the same name mounted at a time in the entire app by ensuring the
name
is unique, or adding an
id
to the name:
```
function Item({id}) {  // ✅ All items will get the same "name".  return
...
;}function ItemList({items}) {  return (    <>      {item.map(item =>
)}      );}
```
이전
<Activity>
다음
API
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