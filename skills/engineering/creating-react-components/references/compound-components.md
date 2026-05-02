## Rule: Compound Components for Related UI Groups

When multiple components share state and belong to the same conceptual UI group (Tabs, Select, Accordion, Dialog, Toggle), implement them as compound components using Context + sub-components attached to the parent.

**Do:**
- Own shared state in the parent; expose it to children via `createContext` + `useContext`
- Attach sub-components as named properties on the parent (`Toggle.On`, `Toggle.Button`)
- Throw a clear error when sub-components are used outside their parent context

**Don't:**
- Thread shared state through props across multiple sibling/child components
- Use `React.Children.map` or `React.cloneElement` to inject props — use Context instead
- Mix compound component state with application-level state

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
