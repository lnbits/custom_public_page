window.app = Vue.createApp({
  el: '#vue',
  mixins: [windowMixin],
  delimiters: ['${', '}'],
  data: function () {
    return {
      currencyOptions: ['sat'],
      settingsFormDialog: {
        show: false,
        data: {}
      },

      pagesFormDialog: {
        show: false,
        data: {
          name: null,
          content: null,
          center: false
        },
        previewHtml: ''
      },
      pagesList: [],
      pagesTable: {
        search: '',
        loading: false,
        columns: [
          {
            name: 'name',
            align: 'left',
            label: 'Name',
            field: 'name',
            sortable: true
          },
          {
            name: 'updated_at',
            align: 'left',
            label: 'Updated At',
            field: 'updated_at',
            sortable: true
          },
          {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true}
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      }
    }
  },
  watch: {
    'pagesTable.search': {
      handler() {
        const props = {}
        if (this.pagesTable.search) {
          props['search'] = this.pagesTable.search
        }
        this.getPages()
      }
    },
    'pagesFormDialog.data.content'(val) {
      this.updatePreview(val, this.pagesFormDialog.data.center)
    },
    'pagesFormDialog.data.center'(val) {
      this.updatePreview(this.pagesFormDialog.data.content, val)
    }
  },

  methods: {
    updatePreview(content, center = false) {
      const source = content || ''
      const markdownHtml = LNbits.utils.convertMarkdown(source)
      const cardAlignment = center ? 'text-align:center;' : 'text-align:left;'
      this.pagesFormDialog.previewHtml = `
<!doctype html>
<html>
  <head>
    <style>
      body {
        margin: 0;
        padding: 16px;
        background: #121212;
        color: #e0e0e0;
        font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
      }
      .container {
        display: flex;
        justify-content: center;
      }
      .card {
        max-width: 520px;
        width: 100%;
        background: #1f1f1f;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px;
        box-sizing: border-box;
        ${cardAlignment}
      }
      h1, h2, h3, h4, h5, h6 { color: #fff; }
      a { color: #29b6f6; }
      pre { background: #111; padding: 12px; border-radius: 6px; overflow: auto; }
      code { font-family: 'Fira Code', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card">
        ${markdownHtml}
      </div>
    </div>
  </body>
</html>`
    },

    //////////////// Pages ////////////////////////
    async showNewPagesForm() {
      this.pagesFormDialog.data = {
        name: 'Shop callback',
        content:
          '# Thanks for your order! \n\n## We aim to ship within 2 working days \n\n<a href="https://shop.lnbits.com">return to shop</a>',
        center: true
      }
      this.updatePreview(
        this.pagesFormDialog.data.content,
        this.pagesFormDialog.data.center
      )
      this.pagesFormDialog.show = true
    },
    async showEditPagesForm(data) {
      this.pagesFormDialog.data = {...{center: false}, ...data}
      this.updatePreview(data.content || '', this.pagesFormDialog.data.center)
      this.pagesFormDialog.show = true
    },
    async savePages() {
      try {
        const data = {extra: {}, ...this.pagesFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        const entry = data.id ? `/${data.id}` : ''
        await LNbits.api.request(
          method,
          '/custom_public_page/api/v1/pages' + entry,
          null,
          data
        )
        this.getPages()
        this.pagesFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },

    async getPages(props) {
      try {
        this.pagesTable.loading = true
        const params = LNbits.utils.prepareFilterQuery(this.pagesTable, props)
        const {data} = await LNbits.api.request(
          'GET',
          `/custom_public_page/api/v1/pages/paginated?${params}`,
          null
        )
        this.pagesList = data.data
        this.pagesTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.pagesTable.loading = false
      }
    },
    async deletePages(pagesId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Pages?')
        .onOk(async () => {
          try {
            await LNbits.api.request(
              'DELETE',
              '/custom_public_page/api/v1/pages/' + pagesId,
              null
            )
            await this.getPages()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },
    async exportPagesCSV() {
      await LNbits.utils.exportCSV(
        this.pagesTable.columns,
        this.pagesList,
        'pages_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },
    dateFromNow(date) {
      return moment(date).fromNow()
    }
  },
  async created() {
    this.getPages()
  }
})
