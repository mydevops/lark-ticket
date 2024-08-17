import axios from 'axios'

let APIPrefix = "/api/v1/web"

export const getConfigs = params => {
    return axios.get(`${APIPrefix}/configs`).then(res => res.data)
}

export const getConfig = approval_code => {
    return axios.get(`${APIPrefix}/config/${approval_code}`).then(res => res.data)
}


export const deleteConfig = approval_code => {
    return axios.delete(`${APIPrefix}/config/${approval_code}`).then(res => res.data)
}

export const updateConfig = data => {
    return axios.put(`${APIPrefix}/config`, data).then(res => res.data)
}

export const createConfig = data => {
    return axios.post(`${APIPrefix}/config`, data).then(res => res.data)
}

export const get_lark_approval_detail = approval_code => {
    return axios.get(`${APIPrefix}/lark/approval?approval_code=${approval_code}`).then(res => res.data)
}
