# React / React Native Style Guide

## Component Directories

**Note:** [Path Aliases](https://reactnative.dev/docs/typescript#using-custom-path-aliases-with-typescript) will be implemented.

  

### Naming

```markdown
react-native-app/
└── navigation/
    ├── RootStackNavigation/
    │   ├── index.ts
    │   ├── RootStackNavigation.tsx
    │   └── types.ts
    └── headers/
        ├── HeaderWithTitle/
        │   ├── index.ts  
        │   └── HeaderWithTitle.tsx
        ├── HeaderWithGradient/
        │   ├── index.ts  
        │   └── HeaderWithGradient.tsx
        └── index.ts
```

  

**snake-case**

When the directory **describes a domain and** **does not** **_directly_** **contain any** `Component.tsx` files

  

*   See **`headers`** in the [example above](https://app.clickup.com/1274576/v/dc/16wpg-151894/16wpg-60080?block=block-feb67929-55c9-4d20-aaf5-b4bbdaab54fa)

  

**PascalCase**

When a directory directly contains a `Component.tsx` file

*   See **`HeaderWithTitle`** and **`RootStackNavigation`** in the example above

  

#### Prefixes

Omit domain-specific prefixes within a directory:

```markdown
react-native-app/
└── screens/
    └── HomeScreen/
        ├── ListItem.tsx ✅
        └── HomeScreenListItem.tsx 🚫
```

  

#### Suffixes

Naming is based on the purpose of the component:

1. `Screen`
2. `Button`
3. `Modal`
4. `List`/`ListItem`
5. `Scroller`
6. `Placeholder`: for skeleton loading
7. ... and more

  

#### Files Exporting a Component

  

**Generally**

*   one file = one Component
*   A file exporting a Component is named 1:1

  

**Example**

1. `CustomButton.tsx` provides a namespace export of a component called `CustomButton`

```typescript
export { CustomButton }; ✅
export default CustomButton; 🚫
export { CustomButton as MyButton }; 🚫
```

1. The name of files exporting Components should be `PascalCase`

```typescript
somePath/CustomButton.tsx ✅
somePath/customButton.tsx 🚫
somePath/custom-button.tsx 🚫
```

  

### Directory Composition

#### Rule of Modularity

Export (from `index.ts` ) **_only what is intended to be used from that directory’s "module"._**

  

#### Example

```markdown
HomeScreen/
├── index.ts
├── HomeScreen.tsx
├── AccountRow.tsx
├── VacationIdeasList/
│   ├── VacationIdeasList.tsx
│   ├── ListItem.tsx
│   ├── CTAButton.tsx
│   └── index.ts
├── constants.ts
├── hooks.ts
├── utils.ts
└── types.ts
```

1. **HomeScreen (module)**
    *   `index.ts`

```typescript
  export * from './HomeScreen' 
  
  // and possibly
  export * from './types
```

*       *   `HomeScreen.tsx`
    *   `AccountRow.tsx`
    *   **VacationIdeasList** (sub-module)
        *   `VacationIdeasList.tsx`
        *   `ListItem.tsx`
        *   `CTAButton.tsx`
        *   `index.ts` has `export * from './VacationIdeasList';`
*       *   `constants.ts` : variables tied to a "business rule"
        *   number of items per page in a list being queried
        *   number of rows in a grid
*       *   `hooks.ts` OR `hooks/` directory
        *   custom hooks specific to the parent module
        *   **Note:** depending on the complexity of the hooks, `hooks` can be, itself, a directory of files, each containing 1 independently-named hook

```markdown
hooks/
├── index.ts
├── useSetScrollPositionFromNavigationParam.ts
└── useBottomSheet.ts
```

*       *   `utils.ts`
        *   utility functions used in the module
*       *   `types.ts`
        *   types common to multiple files in the module
        *   usually, a `types.ts` file is defined to avoid cyclical imports
            *   `HomeScreen` imports from `utils`
            *   `utils` imports types also from `HomeScreen`
            *   cyclical import 🚫

  

#### [Co-Location](https://kentcdodds.com/blog/colocation) (Tests + Storybook Stories)

  

Tests + Stories are co-located with their files:

```markdown
HomeScreen/
├── index.ts
├── HomeScreen.stories.tsx
├── HomeScreen.test.tsx
├── HomeScreen.tsx
├── utils.ts
└── utils.test.ts
```

  

If a file needs additional setup for its test, move into its own directory:

```markdown
HomeScreen/
├── index.ts
├── HomeScreen.stories.tsx
├── HomeScreen.test.tsx
├── HomeScreen.tsx
└── utils/
    ├── index.ts
    ├── utils.ts
    ├── utils.test.ts
    └── mocks.ts
```

# Writing React / React Native

React is powerful! But it's not perfect. There are many viable approaches to writing React, and even the official React docs evolve in parallel with releases (take the [useEffect documentation](https://react.dev/reference/react/useEffect), for example).

  

The following is Utility's approach.

## Optimization

*   Memoize in shared hooks / components
    *   Follow common open-source conventions
        *   Functions passed as props to other Components should be memoized
        *   Callback function returned from a custom hook -- exported from a `module` -- is memoized
        *   Objects (`{}` , `[]` , etc)
    *   Adhering to these rules means `children` can use other rules of `React` -- like dependency arrays -- as intended, without having to wonder whether or not their props are optimized for implementing such patterns
*   Otherwise, in general, **_avoid premature optimizations_**
    *   This means: Do not use `useMemo` or `useCallback` prematurely
    *   Follow the [single responsibility principle](https://www.freecodecamp.org/news/solid-principles-single-responsibility-principle-explained/#:~:text=The%20Single%20Responsibility%20Principle%20(SRP,only%20one%20reason%20to%20change%22.) for hooks, functions, and composable components
    *   If/when performance issues come around, measure the current state of affairs to establish a baseline! _Then,_ optimize:
        *   [Use the Profiler](https://reactnative.dev/docs/profiling), [considering Hermes](https://reactnative.dev/docs/profile-hermes)
        *   [Read the flamegraph](https://www.pluralsight.com/guides/profiling-performance-with-react-developer-tools)
        *   Make small, incremental changes + compare to the baseline; libraries like [Reassure](https://github.com/callstack/reassure) can be used to go one step further with performance regression tests
*   Consider where the component is being used
    *   Components in a screen that is usually at the top of the navigation stack (for example: at the end of a checkout flow) are rendered less than, say, a `HomeScreen`
    *   A component core to the application's UI kit (an `atom` or `molecule` ) has a greater need to be optimized than a one-off component

## Managing Local State

*   **minimal** complexity: utilize `useState`
    *   ≤ 2 state values in reaction to some action
    *   [Use a Union type](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types), instead of multiple booleans
*   **moderate** to complex — use [zustand](https://github.com/pmndrs/zustand) (even if it's not a global/shared state management system)

  

## useEffect

Checkout the [latest](https://react.dev/reference/react/useEffect) [_useEffect_](https://react.dev/reference/react/useEffect) [documentation](https://react.dev/reference/react/useEffect)! Also, see [this section above](https://app.clickup.com/1274576/v/dc/16wpg-76025/16wpg-60080?block=block-ba74a608-66ab-4081-8b22-e7c7ff7c6f28).

*   **minimal** complexity: same file
*   **everything else:** pull the hook out into a separate file + name appropriately
    *   again, see [this section](https://app.clickup.com/1274576/v/dc/16wpg-76025/16wpg-60080?block=block-ba74a608-66ab-4081-8b22-e7c7ff7c6f28) for when to use `hooks.ts` and when to use a `hooks` directory
*   one hook = one responsibility
*   anything within and returned from a custom shared hook [should](https://app.clickup.com/1274576/v/dc/16wpg-76025/16wpg-60080?block=block-dc968033-66a3-410c-b759-0f0856f27723) [be memoized](https://app.clickup.com/1274576/v/dc/16wpg-76025/16wpg-60080?block=block-dc968033-66a3-410c-b759-0f0856f27723)

## Custom Styling

*   **No** **`margin`** ‼️ Some theory/rationale [can be found here](https://mxstbr.com/thoughts/margin/) and in [this podcast](https://designdetails.fm/episodes/5zbXXxsT)
*   Do not inject `*style` props into custom components + extend its styling
    *   Keep each component's implementation as minimal as possible
    *   Wrap the component to add custom styling, if needed

#### Example

*   `SomeListItem.tsx`
    *   should have no `padding` / (and [no](https://app.clickup.com/1274576/v/dc/16wpg-133134/16wpg-60080?block=block-7a0398fa-cbd2-4d29-a608-e56b3ea75ee8) [`margin`](https://app.clickup.com/1274576/v/dc/16wpg-133134/16wpg-60080?block=block-7a0398fa-cbd2-4d29-a608-e56b3ea75ee8) )
    *   in `renderItem`, it's common to wrap it with some `View` from the component library that can apply `padding` based on the theme's globally-defined spacing
*   Of course, for components imported from libraries external to Utility, use their respective styling APIs
    *   Use a function to reference values from the **theme,** though, when using an external library
    *   [Here's an example](https://tamagui.dev/docs/core/styled#:~:text=component%20as%20defaultProps.-,Variants,-Let%27s%20add%20some) from `tamagui` using its exported `styled` function

## Naming

*   Don’t use negative prefixes
    *   either use `!` -- `!isAvailable` OR
    *   an antonym -- `isNotOpened` becomes `isClosed`
*   Use verb prefixes; should be readable in plain English
    *   Good: `isOpened`, `hasItems` ✅
    *   Bad: `doesntClose`, `open` , `opened`, `isNotClosed`, `loggedIn` , `loaded` ❌
*   For what you may initially think to use a flag, consider using a [Union type](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types) instead to be more explicit. For example, a query's lifecycle:

```typescript
🚫
const [isLoading, setIsLoading] = useState(false);
const [hasError, setHasError] = useState(false);

✅
type QueryState = "idle" | "loading" | "error";

const [queryState, setQueryState] = useState<QueryState>("idle");
```

## Conditional Rendering

### Good

```plain
{status ? <Tag>{status}</Tag> : null}
```

### Bad

```plain
{status && <Tag>{status}</Tag>}
```

  

Check out [this blog post](https://kentcdodds.com/blog/use-ternaries-rather-than-and-and-in-jsx) for more information.

  

### React.FC

*   Please do NOT use `React.FC` for typing React components. More information in [here](https://github.com/facebook/create-react-app/pull/8177) and [here](https://fettblog.eu/typescript-react-why-i-dont-use-react-fc/)
*   With that said, [it's "fine" when using Typescript 5.1+](https://www.totaltypescript.com/you-can-stop-hating-react-fc)

## React Navigation

*   Whenever possible, please use elements directly from @react-navigation/elements when implementing custom navigation-related UI
*   Do not use absolute positioning (in elements included in the Navigation UI, and just [**in general**](https://reactnative.dev/docs/layout-props#position)!)

# Writing [TypeScript](https://www.typescriptlang.org/docs/)

## Typecasting

*   Generally speaking: Avoid it
    *   Consider using a [type guard](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)
*   If you must typecast, do it as high as possible in the tree of logic (i.e. when receiving data from an endpoint) and document why you are doing it with a comment
*   Opt for implicit typing over explicit when possible
*   Do not use the `any` type, either implicitly or explicitly

  

## Import/export patterns

*   exports
    *   use named exports (not default)
    *   Add exports to the bottom of the file

```typescript
type FooProps = {};

const FooComponent = ({}: FooProps) => {};

export const { FooComponent };
export type { FooProps };
```

*       *   export types afterwards

  

## Types and Interfaces

*   Use a `type` unless you explicitly need the additional functionality of an `interface`
    *   [Here is an excellent post on type vs interface](https://javascript.plainenglish.io/no-more-confusion-about-typescripts-type-and-interface-63c39418ae35) (open in incognito browser if you cannot access)
*   `type` and `interface` names should be self-documenting
    *   Do **_not_** prefix with `T` or `I`
*   Things should read as plain English; no abbreviations (unless something very common like `API` )
*   When adding functions, prefer the `=>` annotation

```typescript
type Calculator = {
   sum: (left: number, right: number) => number;
   getIsValid?: () => boolean;
}
```

*   When creating typed functions only, use arrow `=>`

```typescript
type Operation = (left: number, right: number) => number;
```

*   Use [intersection types](https://javascript.plainenglish.io/using-typescript-intersection-types-like-a-pro-a55da6a6a5f7) to be more specific about your code. For example:

```typescript
type Function1 = (a: string, b: string) => void;
type Function2 = (a: number, b: number) => void;
type Function3 = (a: number, b: string) => void;

type AnyFunction = Function1 & Function2 & Function3;

const someFunction: AnyFunction = (a: string | number, b: string | number) => {};

someFunction("This", "Works"); ✅
someFunction(10, 5); ✅
someFunction(10, "Also Works"); ✅

// This doesn't work since no function overload defines `a: string, b number`
someFunction("Doesn't work", 5); 🚫
```

## tsc Errors

`tsc` is run in CI/CD a part of the PR pipeline and requiring to pass before the PR can be merged.

  

## Helper functions (utils)

*   synchronous
    *   getters: `get*`
    *   setters: `set*`
    *   functions that create data of a certain shape: `create*`
*   api functions
    *   `post*`
    *   `patch*`
    *   `fetch*`
    *   `delete*`
*   [type guards](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates): `is*` or `are*`

  

# Libraries

## State Management

*   [@tanstack/react-query](https://tanstack.com/query/v4): for keeping api and client state in sync
*   [Local State](https://app.clickup.com/1274576/v/dc/16wpg-76025/16wpg-60080?block=block-65104c5e-3754-4fb0-9568-964ebedd354c)
    *   [zustand](https://github.com/pmndrs/zustand)

## Date/Time

*   [date-fns](https://date-fns.org/)

## Networking

*   [@tanstack/react-query](https://tanstack.com/query/v4)
*   [axios](https://github.com/qiangmao/axios)
*   [Orval](https://orval.dev/) for automatic code generation (works with `axios` and `@tanstack/react-query` )

## Environment Management

*   [react-native-ultimate-config](https://github.com/maxkomarychev/react-native-ultimate-config)
*   [Doppler](https://www.doppler.com/)

  

# CI/CD

## Managing Secrets

Utility uses [Doppler](https://www.doppler.com/) to manage secrets. This includes both sensitive and non-sensitive information:

*   sensitive
    *   Apple API key (`app_store_key.json` )
    *   GitHub private token
*   non-sensitive
    *   used in the app client code
    *   i.e. an analytics client key

We add a Doppler token to GitHub Secrets to be able to inject the values into the `process.env` + use in GitHub Actions.

## PRs

When a PR goes up, we generally run `tsc` and `eslint` jobs to ensure code quality. These jobs run off the same rules being applied locally in your IDE, but we all make the occasional mistake and forget to remove unused imports!

  

Once it's merged, a deployment is usually triggered based on the target branch.

## Deployment Types

*   **qa ➝** an internal build distributed with TestFlight and Google Play internal testing
    *   usually, we use the Utility accounts for `qa` , not the client's account
*   **staging** ➝ a client-facing build distributed with TestFlight and Google Play internal testing
    *   usually, we use the Client's accounts for `staging`, not Utility's
*   **production ➝** a client-facing build distributed using TestFlight and [Google Play internal testing](https://play.google.com/console/about/internal-testing/)
    *   we use the Client's accounts for `production`, not Utility's

# Environment Management

## Environment Types

Utility has three environments for any given project:

*   qa ➝ `qa` branch
*   staging ➝ `staging` branch
*   prod ➝ `main` branch

  

## Developing

*   Development is generally done against the `qa` environment
*   The general process of maintaining environment variables is handled by [Doppler](https://www.doppler.com/)
*   The general process for managing changing between environments is handled by [react-native-ultimate-config](https://github.com/maxkomarychev/react-native-ultimate-config)
*   The general steps to set an environment and build the app can be found in the Closet documentation
    *   TODO