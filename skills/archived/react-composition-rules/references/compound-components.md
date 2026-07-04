## Rule: Compound Components for Related UI Groups

Multiple components share state + same conceptual UI group (Tabs, Select, Accordion, Dialog, Toggle) → use compound components via Context + sub-components attached to parent.

**Do:**

- Own shared state in parent; expose to children via `createContext` + `useContext`
- Attach sub-components as named properties on parent (`Toggle.On`, `Toggle.Button`)
- Throw clear error when sub-components used outside parent context

**Don't:**

- Thread shared state through props across sibling/child components
- Use `React.Children.map` or `React.cloneElement` to inject props — use Context
- Mix compound component state with app-level state

**Example:**

```tsx
// bad
<Tabs activeTab={tab} onTabChange={setTab}>
  <TabList activeTab={tab} onTabChange={setTab} tabs={tabs} />
  <TabPanel activeTab={tab} content={content} />
</Tabs>

// good
<Tabs>
  <Tabs.List>
    <Tabs.Tab value="a">Tab A</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="a">Content A</Tabs.Panel>
</Tabs>
```
