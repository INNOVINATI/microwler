export const state = () => ({
  host: null,
  projects: [],
  chartData: null
})

export const getters = {
  getProjectByName: state => name => state.projects.find(p => p.name === name),
  getCacheSize: state => {
    let size = 0
    state.projects.forEach(project => {
      if (!!project.cache)
        size += project.cache.length
    })
    return size
  }
}


export const actions = {
  connect({commit, dispatch}, host) {
    fetch(`http://${host}/status`)
      .then(async res => await res.json())
      .then(data => {
        commit('connect', {
          domain: host,
          status: data.app,
          projects: data.projects
        })
      })
      .catch(err => {
        this.connecting = false
        this.domain = null
        alert(err)
      })
  },
  getProject({ state, commit, dispatch }, project) {
    fetch(`http://${state.host.domain}/status/${project}`)
      .then(res => res.json())
      .then(data => {
        commit('addProject', {
          name: project,
          startUrl: data.start_url,
          lastRun: data.last_run,
          cache: null
        })
        return dispatch('getCache', project)
      })
  },
  getCache({ state, commit, dispatch}, project) {
    return fetch(`http://${state.host.domain}/data/${project}`)
      .then(res => res.json())
      .then(data => commit('loadProjectCache', {name: project, cache: data.data}))
  },
  runProject({ state, commit }, project) {
    return fetch(`http://${state.host.domain}/crawl/${project}`)
      .then(res => res.json())
      .then(data => commit('loadResults', {name: project, results: data.data}))
  },
  updateChart({ getters, commit }, projectName) {
    let history = {}
    let project = getters.getProjectByName(projectName)
    for (let page of project.cache)
      history[page.discovered] = history.hasOwnProperty(page.discovered) ? history[page.discovered] + 1 : 1
    commit('updateChart', Object.values(history))
  }
}


export const mutations = {
  connect(state, host) {
    state.host = host
  },
  addProject(state, project) {
    const idx = state.projects.findIndex(p => project.name === project)
    if (idx !== -1)
      state.projects.splice(idx, 1)
    state.projects.push(project)
  },
  loadProjectCache(state, {name, cache}) {
    state.projects.find(p => p.name === name).cache = cache
  },
  loadResults(state, {name, results}) {
    state.projects.find(p => p.name === name).latestResults = results
  },
  flush(state) {
    state.projects = []
  },
  updateChart(state, data) {
    state.chartData = data
  }
}
