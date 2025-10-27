<template>
  <div class="landing-config-admin">
    <AdminLayout
      page-title="Configuración del Sitio"
      :breadcrumbs="[{ label: 'Configuración del Sitio' }]"
    >
      <div class="row py-3">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <!-- Success Message -->
              <div
                v-if="successMessage"
                class="alert alert-success alert-dismissible fade show"
                role="alert"
              >
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
                <button
                  type="button"
                  class="btn-close"
                  @click="successMessage = ''"
                  aria-label="Close"
                ></button>
              </div>

              <!-- Configuration Form -->
              <form v-else @submit.prevent="saveConfiguration">
                <div class="dynamic-content-header mb-4">
                  <h5 class="text-primary mb-2">
                    <i class="bi bi-list-stars me-2"></i>
                    Contenido Dinámico de la Página
                  </h5>
                  <div class="alert alert-info d-flex align-items-start">
                    <i class="bi bi-info-circle-fill me-3 fs-5"></i>
                    <div>
                      <strong>¿Qué es esto?</strong>
                      <p class="mb-0 small">
                        Aquí podés editar las diferentes secciones de texto que aparecen en la
                        página principal. Cada sección tiene un formato específico que debés seguir.
                        <strong>No te preocupes</strong>, hay ejemplos debajo de cada campo que
                        podés copiar y modificar.
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Basic Information Section -->
                <div class="config-section-card mb-4">
                  <div class="config-section-header" @click="toggleSection('basicInfo')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-info-circle me-2 text-primary"></i>
                      <h5 class="mb-0">Información Básica</h5>
                    </div>
                    <i
                      :class="[
                        'bi',
                        expandedSections.basicInfo ? 'bi-chevron-up' : 'bi-chevron-down',
                      ]"
                    ></i>
                  </div>
                  <div v-show="expandedSections.basicInfo" class="config-section-body">
                    <div class="row">
                      <div class="col-lg-6 mb-3">
                        <label for="page_title" class="form-label"
                          ><i class="bi bi-window me-1"></i>Título de la Página</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          id="page_title"
                          v-model="formData.page_title"
                          placeholder="Ej: Sistema de Voluntariado"
                          maxlength="100"
                        />
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Aparece en la pestaña del navegador
                        </div>
                      </div>

                      <div class="col-lg-6 mb-3">
                        <label for="site_name" class="form-label"
                          ><i class="bi bi-building me-1"></i>Nombre del Sitio</label
                        >
                        <input
                          type="text"
                          class="form-control"
                          id="site_name"
                          v-model="formData.site_name"
                          placeholder="Ej: Voluntariado UNCuyo"
                          maxlength="100"
                        />
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Aparece en el header y navegación
                        </div>
                      </div>

                      <div class="col-12 mb-3">
                        <label for="welcome_message" class="form-label"
                          ><i class="bi bi-chat-heart me-1"></i>Mensaje de Bienvenida</label
                        >
                        <textarea
                          class="form-control"
                          id="welcome_message"
                          v-model="formData.welcome_message"
                          rows="3"
                          placeholder="Ej: Convertite en el cambio que querés ver."
                        ></textarea>
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Título principal de la página de inicio
                        </div>
                      </div>

                      <div class="col-12 mb-0">
                        <label for="description" class="form-label"
                          ><i class="bi bi-text-paragraph me-1"></i>Descripción</label
                        >
                        <textarea
                          class="form-control"
                          id="description"
                          v-model="formData.description"
                          rows="3"
                          placeholder="Ej: ¡Sumáte a los voluntariados!"
                        ></textarea>
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Subtítulo de la página de inicio y descripción SEO
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Contact & Media Section -->
                <div class="config-section-card mb-4">
                  <div class="config-section-header" @click="toggleSection('contactMedia')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-envelope me-2 text-primary"></i>
                      <h5 class="mb-0">Contacto y Medios</h5>
                    </div>
                    <i
                      :class="[
                        'bi',
                        expandedSections.contactMedia ? 'bi-chevron-up' : 'bi-chevron-down',
                      ]"
                    ></i>
                  </div>
                  <div v-show="expandedSections.contactMedia" class="config-section-body">
                    <div class="row">
                      <div class="col-lg-6 mb-3">
                        <label for="contact_email" class="form-label"
                          ><i class="bi bi-envelope-at me-1"></i>Email de Contacto</label
                        >
                        <input
                          type="email"
                          class="form-control"
                          id="contact_email"
                          v-model="formData.contact_email"
                          placeholder="Ej: contacto@voluntariado.uncuyo.edu.ar"
                        />
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Aparece en el footer del sitio
                        </div>
                      </div>

                      <div class="col-lg-6 mb-3">
                        <label for="phone_number" class="form-label"
                          ><i class="bi bi-telephone me-1"></i>Número de Teléfono</label
                        >
                        <input
                          type="tel"
                          class="form-control"
                          id="phone_number"
                          v-model="formData.phone_number"
                          placeholder="Ej: +542614123456"
                          pattern="^\+?1?\d{9,15}$"
                        />
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Formato: +542614123456
                        </div>
                      </div>

                      <div class="col-lg-6 mb-3">
                        <label for="instagram_handle" class="form-label"
                          ><i class="bi bi-instagram me-1"></i>Instagram</label
                        >
                        <div class="input-group">
                          <span class="input-group-text">@</span>
                          <input
                            type="text"
                            class="form-control"
                            id="instagram_handle"
                            v-model="formData.instagram_handle"
                            placeholder="voluntariado_uncuyo"
                            pattern="^[a-zA-Z0-9_.]+$"
                            maxlength="50"
                          />
                        </div>
                        <div class="form-text">
                          <i class="bi bi-info-circle me-1"></i>
                          Solo letras, números, puntos y guiones bajos
                        </div>
                      </div>

                      <div class="col-lg-6 mb-0">
                        <label for="hero_image" class="form-label"
                          ><i class="bi bi-image me-1"></i>Imagen Principal</label
                        >
                        <input
                          type="file"
                          class="form-control"
                          id="hero_image"
                          @change="handleFileChange"
                          accept="image/*"
                        />
                        <div class="form-text">
                          <div
                            v-if="formData.hero_image && typeof formData.hero_image === 'string'"
                          >
                            <i class="bi bi-file-image text-success me-1"></i>
                            Archivo actual: {{ getImageFileName() }}
                          </div>
                          <div v-else-if="selectedFile">
                            <i class="bi bi-upload text-primary me-1"></i>
                            Nuevo archivo: {{ selectedFile.name }}
                          </div>
                          <div v-else>
                            <i class="bi bi-info-circle me-1"></i>
                            Selecciona una imagen para la página principal
                          </div>
                        </div>
                        <!-- Image Preview -->
                        <div
                          v-if="
                            (formData.hero_image && typeof formData.hero_image === 'string') ||
                            imagePreview
                          "
                          class="image-preview-container mt-2"
                        >
                          <img
                            :src="imagePreview || formData.hero_image"
                            alt="Vista previa"
                            class="image-preview"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Footer Configuration Section -->
                <div class="config-section-card mb-4">
                  <div class="config-section-header" @click="toggleSection('footerConfig')">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-layout-text-window me-2 text-primary"></i>
                      <h5 class="mb-0">Configuración del Footer</h5>
                    </div>
                    <i
                      :class="[
                        'bi',
                        expandedSections.footerConfig ? 'bi-chevron-up' : 'bi-chevron-down',
                      ]"
                    ></i>
                  </div>
                  <div v-show="expandedSections.footerConfig" class="config-section-body">
                    <div class="mb-0">
                      <label for="footer_text" class="form-label"
                        ><i class="bi bi-c-circle me-1"></i>Texto del Footer</label
                      >
                      <textarea
                        class="form-control"
                        id="footer_text"
                        v-model="formData.footer_text"
                        rows="2"
                        placeholder="Ej: © 2025 Universidad Nacional de Cuyo. Todos los derechos reservados."
                      ></textarea>
                      <div class="form-text">
                        <i class="bi bi-info-circle me-1"></i>
                        Texto de copyright que aparece en el pie de página
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Dynamic Content Configuration -->
                <div class="row mt-4">
                  <div class="col-12">
                    <!-- Info Items -->
                    <div class="dynamic-field-card mb-4">
                      <div class="dynamic-field-header" @click="toggleSection('infoItems')">
                        <div class="d-flex align-items-center">
                          <i class="bi bi-info-square me-2 text-primary"></i>
                          <h6 class="mb-0">Items de Información ("¿Qué es el Voluntariado?")</h6>
                        </div>
                        <i
                          :class="[
                            'bi',
                            expandedSections.infoItems ? 'bi-chevron-up' : 'bi-chevron-down',
                          ]"
                        ></i>
                      </div>
                      <div v-show="expandedSections.infoItems" class="dynamic-field-body">
                        <div class="mb-3">
                          <p class="text-muted small mb-2">
                            <i class="bi bi-lightbulb-fill me-1"></i>
                            Define las tarjetas informativas que explican qué es el voluntariado.
                            Cada item necesita un ícono, un título y una descripción.
                          </p>
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-secondary me-2"
                            @click="loadExample('info_items')"
                          >
                            <i class="bi bi-file-earmark-text me-1"></i>
                            Cargar Ejemplo
                          </button>
                          <button type="button" class="btn btn-sm btn-success" @click="addInfoItem">
                            <i class="bi bi-plus-circle me-1"></i>
                            Agregar Item
                          </button>
                        </div>

                        <!-- Info Items List -->
                        <div
                          v-for="(item, index) in infoItems"
                          :key="index"
                          class="form-item-card mb-3"
                        >
                          <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="mb-0">Item {{ index + 1 }}</h6>
                            <button
                              type="button"
                              class="btn btn-sm btn-danger"
                              @click="removeInfoItem(index)"
                            >
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>

                          <div class="row">
                            <div class="col-md-6 mb-3">
                              <label :for="`info_icon_${index}`" class="form-label">Ícono</label>
                              <select
                                :id="`info_icon_${index}`"
                                class="form-select icon-select"
                                v-model="item.icon"
                              >
                                <option
                                  v-for="iconOpt in availableIcons"
                                  :key="iconOpt.value"
                                  :value="iconOpt.value"
                                >
                                  {{ iconOpt.label }}
                                </option>
                              </select>
                              <div class="icon-preview mt-2">
                                <i :class="['bi', item.icon, 'icon-preview-large']"></i>
                                <span class="text-muted small ms-2">Vista previa del ícono</span>
                              </div>
                            </div>
                            <div class="col-md-6 mb-3">
                              <label :for="`info_title_${index}`" class="form-label">Título</label>
                              <input
                                type="text"
                                :id="`info_title_${index}`"
                                class="form-control"
                                v-model="item.title"
                                placeholder="Ej: Iniciativa"
                              />
                            </div>
                          </div>
                          <div class="mb-0">
                            <label :for="`info_desc_${index}`" class="form-label"
                              >Descripción</label
                            >
                            <textarea
                              :id="`info_desc_${index}`"
                              class="form-control"
                              v-model="item.description"
                              rows="3"
                              placeholder="Describe este aspecto del voluntariado..."
                            ></textarea>
                          </div>
                        </div>

                        <div v-if="infoItems.length === 0" class="alert alert-warning">
                          <i class="bi bi-exclamation-triangle me-2"></i>
                          No hay items agregados. Haz clic en "Agregar Item" o "Cargar Ejemplo".
                        </div>
                      </div>
                    </div>

                    <!-- Testimonials -->
                    <div class="dynamic-field-card mb-4">
                      <div class="dynamic-field-header" @click="toggleSection('testimonials')">
                        <div class="d-flex align-items-center">
                          <i class="bi bi-chat-quote me-2 text-primary"></i>
                          <h6 class="mb-0">Testimonios de Voluntarios</h6>
                        </div>
                        <i
                          :class="[
                            'bi',
                            expandedSections.testimonials ? 'bi-chevron-up' : 'bi-chevron-down',
                          ]"
                        ></i>
                      </div>
                      <div v-show="expandedSections.testimonials" class="dynamic-field-body">
                        <div class="mb-3">
                          <p class="text-muted small mb-2">
                            <i class="bi bi-lightbulb-fill me-1"></i>
                            Agrega testimonios de voluntarios. Cada testimonio incluye nombre, rol,
                            texto y opcionalmente una imagen.
                          </p>
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-secondary mb-2"
                            @click="loadExample('testimonials')"
                          >
                            <i class="bi bi-file-earmark-text me-1"></i>
                            Cargar Ejemplo
                          </button>
                        </div>

                        <!-- Testimonials Form -->
                        <div
                          v-for="(testimonial, index) in testimonials"
                          :key="index"
                          class="form-item-card mb-3"
                        >
                          <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0">
                              <i class="bi bi-chat-quote me-1"></i>
                              Testimonio {{ index + 1 }}
                            </h6>
                            <button
                              type="button"
                              class="btn btn-sm btn-outline-danger"
                              @click="removeTestimonial(index)"
                            >
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>

                          <div class="row">
                            <div class="col-md-6 mb-3">
                              <label class="form-label">Nombre</label>
                              <input
                                type="text"
                                class="form-control"
                                v-model="testimonial.name"
                                placeholder="Nombre del voluntario"
                              />
                            </div>
                            <div class="col-md-6 mb-3">
                              <label class="form-label">Rol</label>
                              <input
                                type="text"
                                class="form-control"
                                v-model="testimonial.role"
                                placeholder="Ej: Voluntario 2023"
                              />
                            </div>
                          </div>

                          <div class="mb-3">
                            <label class="form-label">Testimonio</label>
                            <textarea
                              class="form-control"
                              v-model="testimonial.text"
                              rows="3"
                              placeholder="Escribe el testimonio..."
                            ></textarea>
                          </div>

                          <div class="mb-3">
                            <label class="form-label"
                              ><i class="bi bi-image me-1"></i>Imagen (opcional)</label
                            >
                            <div class="btn-group d-flex mb-2" role="group">
                              <input
                                type="radio"
                                class="btn-check"
                                :id="`testimonial-file-${index}`"
                                :name="`testimonial-upload-${index}`"
                                value="file"
                                v-model="testimonial.uploadType"
                                autocomplete="off"
                              />
                              <label
                                class="btn btn-outline-primary"
                                :for="`testimonial-file-${index}`"
                              >
                                <i class="bi bi-upload me-1"></i>
                                Subir Archivo
                              </label>

                              <input
                                type="radio"
                                class="btn-check"
                                :id="`testimonial-url-${index}`"
                                :name="`testimonial-upload-${index}`"
                                value="url"
                                v-model="testimonial.uploadType"
                                autocomplete="off"
                              />
                              <label
                                class="btn btn-outline-primary"
                                :for="`testimonial-url-${index}`"
                              >
                                <i class="bi bi-link-45deg me-1"></i>
                                URL de Imagen
                              </label>
                            </div>

                            <input
                              v-if="testimonial.uploadType === 'file'"
                              type="file"
                              class="form-control"
                              @change="handleTestimonialImageChange($event, index)"
                              accept="image/*"
                            />
                            <input
                              v-else
                              type="text"
                              class="form-control"
                              v-model="testimonial.imageUrl"
                              placeholder="https://ejemplo.com/foto.jpg"
                            />
                            <div v-if="testimonial.imageUrl" class="image-preview-container mt-2">
                              <img
                                :src="testimonial.imageUrl"
                                alt="Preview"
                                class="image-preview"
                              />
                            </div>
                          </div>
                        </div>

                        <button
                          type="button"
                          class="btn btn-outline-primary"
                          @click="addTestimonial"
                        >
                          <i class="bi bi-plus-circle me-1"></i>
                          Agregar Testimonio
                        </button>
                      </div>
                    </div>

                    <!-- How It Works Steps -->
                    <div class="dynamic-field-card mb-4">
                      <div class="dynamic-field-header" @click="toggleSection('howItWorksSteps')">
                        <div class="d-flex align-items-center">
                          <i class="bi bi-list-ol me-2 text-primary"></i>
                          <h6 class="mb-0">Pasos "Cómo Funciona"</h6>
                        </div>
                        <i
                          :class="[
                            'bi',
                            expandedSections.howItWorksSteps ? 'bi-chevron-up' : 'bi-chevron-down',
                          ]"
                        ></i>
                      </div>
                      <div v-show="expandedSections.howItWorksSteps" class="dynamic-field-body">
                        <div class="mb-3">
                          <p class="text-muted small mb-2">
                            <i class="bi bi-lightbulb-fill me-1"></i>
                            Define los pasos que explican cómo funciona el sistema de voluntariado.
                            Cada paso tiene un título y una descripción.
                          </p>
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-secondary mb-2"
                            @click="loadExample('how_it_works_steps')"
                          >
                            <i class="bi bi-file-earmark-text me-1"></i>
                            Cargar Ejemplo
                          </button>
                        </div>

                        <!-- How It Works Steps Form -->
                        <div
                          v-for="(step, index) in howItWorksSteps"
                          :key="index"
                          class="form-item-card mb-3"
                        >
                          <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0">
                              <i class="bi bi-list-ol me-1"></i>
                              Paso {{ index + 1 }}
                            </h6>
                            <button
                              type="button"
                              class="btn btn-sm btn-outline-danger"
                              @click="removeStep(index)"
                            >
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>

                          <div class="mb-3">
                            <label class="form-label">Título del Paso</label>
                            <input
                              type="text"
                              class="form-control"
                              v-model="step.title"
                              :placeholder="`${index + 1}. Título del paso`"
                            />
                          </div>

                          <div class="mb-2">
                            <label class="form-label">Descripción</label>
                            <textarea
                              class="form-control"
                              v-model="step.description"
                              rows="3"
                              placeholder="Describe este paso..."
                            ></textarea>
                          </div>
                        </div>

                        <button type="button" class="btn btn-outline-primary" @click="addStep">
                          <i class="bi bi-plus-circle me-1"></i>
                          Agregar Paso
                        </button>
                      </div>
                    </div>

                    <!-- Team Members -->
                    <div class="dynamic-field-card mb-4">
                      <div class="dynamic-field-header" @click="toggleSection('teamMembers')">
                        <div class="d-flex align-items-center">
                          <i class="bi bi-people me-2 text-primary"></i>
                          <h6 class="mb-0">Miembros del Equipo</h6>
                        </div>
                        <i
                          :class="[
                            'bi',
                            expandedSections.teamMembers ? 'bi-chevron-up' : 'bi-chevron-down',
                          ]"
                        ></i>
                      </div>
                      <div v-show="expandedSections.teamMembers" class="dynamic-field-body">
                        <div class="mb-3">
                          <p class="text-muted small mb-2">
                            <i class="bi bi-lightbulb-fill me-1"></i>
                            Lista los miembros del equipo que coordinan los voluntariados. Cada
                            miembro tiene nombre, cargo y opcionalmente una foto.
                          </p>
                          <button
                            type="button"
                            class="btn btn-sm btn-outline-secondary mb-2"
                            @click="loadExample('team_members')"
                          >
                            <i class="bi bi-file-earmark-text me-1"></i>
                            Cargar Ejemplo
                          </button>
                        </div>

                        <!-- Team Members Form -->
                        <div
                          v-for="(member, index) in teamMembers"
                          :key="index"
                          class="form-item-card mb-3"
                        >
                          <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0">
                              <i class="bi bi-person me-1"></i>
                              Miembro {{ index + 1 }}
                            </h6>
                            <button
                              type="button"
                              class="btn btn-sm btn-outline-danger"
                              @click="removeTeamMember(index)"
                            >
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>

                          <div class="row">
                            <div class="col-md-6 mb-3">
                              <label class="form-label">Nombre</label>
                              <input
                                type="text"
                                class="form-control"
                                v-model="member.name"
                                placeholder="Nombre del miembro"
                              />
                            </div>
                            <div class="col-md-6 mb-3">
                              <label class="form-label">Cargo</label>
                              <input
                                type="text"
                                class="form-control"
                                v-model="member.role"
                                placeholder="Ej: Coordinador General"
                              />
                            </div>
                          </div>

                          <div class="mb-2">
                            <label class="form-label"
                              ><i class="bi bi-image me-1"></i>Foto (opcional)</label
                            >
                            <div class="btn-group d-flex mb-2" role="group">
                              <input
                                type="radio"
                                class="btn-check"
                                :id="`member-file-${index}`"
                                :name="`member-upload-${index}`"
                                value="file"
                                v-model="member.uploadType"
                                autocomplete="off"
                              />
                              <label class="btn btn-outline-primary" :for="`member-file-${index}`">
                                <i class="bi bi-upload me-1"></i>
                                Subir Archivo
                              </label>

                              <input
                                type="radio"
                                class="btn-check"
                                :id="`member-url-${index}`"
                                :name="`member-upload-${index}`"
                                value="url"
                                v-model="member.uploadType"
                                autocomplete="off"
                              />
                              <label class="btn btn-outline-primary" :for="`member-url-${index}`">
                                <i class="bi bi-link-45deg me-1"></i>
                                URL de Imagen
                              </label>
                            </div>

                            <input
                              v-if="member.uploadType === 'file'"
                              type="file"
                              class="form-control"
                              @change="handleTeamMemberImageChange($event, index)"
                              accept="image/*"
                            />
                            <input
                              v-else
                              type="text"
                              class="form-control"
                              v-model="member.imageUrl"
                              placeholder="https://ejemplo.com/foto.jpg"
                            />
                            <div v-if="member.imageUrl" class="image-preview-container mt-2">
                              <img :src="member.imageUrl" alt="Preview" class="image-preview" />
                            </div>
                          </div>
                        </div>

                        <button
                          type="button"
                          class="btn btn-outline-primary"
                          @click="addTeamMember"
                        >
                          <i class="bi bi-plus-circle me-1"></i>
                          Agregar Miembro
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                  <button type="button" class="btn btn-outline-secondary" @click="resetForm">
                    <i class="bi bi-arrow-clockwise me-1"></i>
                    Resetear
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span
                      v-if="saving"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                    ></span>
                    <i v-else class="bi bi-check-lg me-1"></i>
                    {{ saving ? "Guardando..." : "Guardar Configuración" }}
                  </button>
                </div>
                <ConfirmationModal
                  :show="showResetModal"
                  title="Confirmar reseteo"
                  message="¿Estás seguro de que quieres resetear el formulario?"
                  description="Se perderán los cambios no guardados."
                  confirmText="Resetear"
                  cancelText="Cancelar"
                  type="warning"
                  @confirm="handleResetConfirm"
                  @cancel="handleResetCancel"
                />
              </form>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AdminLayout from "@/components/admin/AdminLayout.vue";
import ConfirmationModal from "@/components/admin/ConfirmationModal.vue";
import { landingConfigAPI } from "@/services/api";
import { useLandingConfig } from "@/composables/useLandingConfig";

export default defineComponent({
  name: "LandingConfigAdmin",
  components: {
    AdminLayout,
    ConfirmationModal,
  },
  setup() {
    const { landingConfig, fetchLandingConfig } = useLandingConfig();
    return {
      sharedLandingConfig: landingConfig,
      refreshLandingConfig: fetchLandingConfig,
    };
  },
  data() {
    return {
      loading: true,
      saving: false,
      error: "",
      successMessage: "",
      selectedFile: null as File | null,
      imagePreview: "" as string,
      showResetModal: false,
      formData: {
        page_title: "",
        site_name: "",
        welcome_message: "",
        description: "",
        contact_email: "",
        phone_number: "",
        instagram_handle: "",
        hero_image: "",
        footer_text: "",
      },
      // Dynamic content fields as structured arrays
      infoItems: [] as Array<{ icon: string; title: string; description: string }>,
      testimonials: [] as Array<{
        name: string;
        role: string;
        text: string;
        imageUrl?: string;
        uploadType?: string;
        imageFile?: File;
      }>,
      howItWorksSteps: [] as Array<{ title: string; description: string }>,
      teamMembers: [] as Array<{
        name: string;
        role: string;
        imageUrl?: string;
        uploadType?: string;
        imageFile?: File;
      }>,
      // UI state for collapsible sections
      expandedSections: {
        basicInfo: true,
        contactMedia: true,
        footerConfig: false,
        infoItems: true,
        testimonials: false,
        howItWorksSteps: false,
        teamMembers: false,
      },
      // Available icons for info items
      availableIcons: [
        { value: "bi-lightbulb", label: "Bombilla (Idea)", class: "bi-lightbulb" },
        { value: "bi-trophy", label: "Trofeo (Logro)", class: "bi-trophy" },
        { value: "bi-flag", label: "Bandera (Meta)", class: "bi-flag" },
        { value: "bi-people", label: "Personas (Comunidad)", class: "bi-people" },
        { value: "bi-heart", label: "Corazón (Pasión)", class: "bi-heart" },
        { value: "bi-star", label: "Estrella (Excelencia)", class: "bi-star" },
        { value: "bi-gear", label: "Engranaje (Proceso)", class: "bi-gear" },
        { value: "bi-book", label: "Libro (Aprendizaje)", class: "bi-book" },
        { value: "bi-globe", label: "Globo (Mundial)", class: "bi-globe" },
        { value: "bi-shield-check", label: "Escudo (Seguridad)", class: "bi-shield-check" },
      ],
    };
  },
  async mounted() {
    await this.loadConfiguration();
  },
  methods: {
    async loadConfiguration() {
      this.loading = true;
      this.error = "";

      try {
        const response = await landingConfigAPI.getConfig();
        if (response.data) {
          this.formData = {
            page_title: response.data.page_title || "",
            site_name: response.data.site_name || "",
            welcome_message: response.data.welcome_message || "",
            description: response.data.description || "",
            contact_email: response.data.contact_email || "",
            phone_number: response.data.phone_number || "",
            instagram_handle: response.data.instagram_handle || "",
            hero_image: response.data.hero_image || "",
            footer_text: response.data.footer_text || "",
          };
          // Load dynamic content as structured arrays
          this.infoItems = response.data.info_items || [];
          this.testimonials = response.data.testimonials || [];
          this.howItWorksSteps = response.data.how_it_works_steps || [];
          this.teamMembers = response.data.team_members || [];
        }
      } catch (err: unknown) {
        console.error("Error loading landing config:", err);
        const error = err as { response?: { data?: { detail?: string } } };
        this.error = error.response?.data?.detail || "Error al cargar la configuración";
      } finally {
        this.loading = false;
      }
    },

    async saveConfiguration() {
      this.saving = true;
      this.error = "";
      this.successMessage = "";

      try {
        const updateData: Record<string, unknown> = {
          page_title: this.formData.page_title,
          site_name: this.formData.site_name,
          welcome_message: this.formData.welcome_message,
          description: this.formData.description,
          contact_email: this.formData.contact_email,
          phone_number: this.formData.phone_number,
          instagram_handle: this.formData.instagram_handle,
          footer_text: this.formData.footer_text,
          info_items: this.infoItems,
          testimonials: this.testimonials,
          how_it_works_steps: this.howItWorksSteps,
          team_members: this.teamMembers,
        };

        // If there's a selected file, include it
        if (this.selectedFile) {
          updateData.hero_image = this.selectedFile;
        }

        const response = await landingConfigAPI.updateConfig(updateData);

        if (response.data) {
          this.successMessage = "Configuración guardada exitosamente";

          // Update form data with response
          this.formData = {
            page_title: response.data.page_title || "",
            site_name: response.data.site_name || "",
            welcome_message: response.data.welcome_message || "",
            description: response.data.description || "",
            contact_email: response.data.contact_email || "",
            phone_number: response.data.phone_number || "",
            instagram_handle: response.data.instagram_handle || "",
            hero_image: response.data.hero_image || "",
            footer_text: response.data.footer_text || "",
          };
          this.infoItems = response.data.info_items || [];
          this.testimonials = response.data.testimonials || [];
          this.howItWorksSteps = response.data.how_it_works_steps || [];
          this.teamMembers = response.data.team_members || [];

          // Clear selected file after successful upload
          this.selectedFile = null;
          this.imagePreview = "";
          const fileInput = document.getElementById("hero_image") as HTMLInputElement;
          if (fileInput) fileInput.value = "";

          // Refresh the shared landing config to update all components
          await this.refreshLandingConfig();

          // Auto-hide success message after 5 seconds
          setTimeout(() => {
            this.successMessage = "";
          }, 5000);
        }
      } catch (err: unknown) {
        console.error("Error saving landing config:", err);
        const error = err as { response?: { data?: { detail?: string } } };
        this.error = error.response?.data?.detail || "Error al guardar la configuración";
      } finally {
        this.saving = false;
      }
    },

    handleFileChange(event: Event) {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        this.selectedFile = target.files[0];

        // Validate file type
        const allowedTypes = [
          "image/jpeg",
          "image/jpg",
          "image/png",
          "image/gif",
          "image/webp",
          "image/svg+xml",
        ];
        if (!allowedTypes.includes(this.selectedFile.type)) {
          this.error =
            "Tipo de archivo no válido. Solo se permiten imágenes (JPEG, PNG, GIF, WebP, SVG)";
          this.selectedFile = null;
          this.imagePreview = "";
          target.value = "";
          return;
        }

        // Validate file size (10MB max)
        if (this.selectedFile.size > 10 * 1024 * 1024) {
          this.error = "El archivo es demasiado grande. Tamaño máximo: 10MB";
          this.selectedFile = null;
          this.imagePreview = "";
          target.value = "";
          return;
        }

        // Create image preview
        const reader = new FileReader();
        reader.onload = (e: ProgressEvent<FileReader>) => {
          if (e.target?.result) {
            this.imagePreview = e.target.result as string;
          }
        };
        reader.readAsDataURL(this.selectedFile);

        this.error = "";
      }
    },

    getImageFileName() {
      if (this.formData.hero_image && typeof this.formData.hero_image === "string") {
        return this.formData.hero_image.split("/").pop() || "archivo_actual";
      }
      return "";
    },

    resetForm() {
      this.showResetModal = true;
    },
    handleResetConfirm() {
      this.loadConfiguration();
      this.selectedFile = null;
      this.imagePreview = "";
      const fileInput = document.getElementById("hero_image") as HTMLInputElement;
      if (fileInput) fileInput.value = "";
      this.error = "";
      this.successMessage = "";
      this.showResetModal = false;
    },
    handleResetCancel() {
      this.showResetModal = false;
    },

    toggleSection(section: keyof typeof this.expandedSections) {
      this.expandedSections[section] = !this.expandedSections[section];
    },

    // Info Items methods
    addInfoItem() {
      this.infoItems.push({ icon: "bi-lightbulb", title: "", description: "" });
    },
    removeInfoItem(index: number) {
      this.infoItems.splice(index, 1);
    },

    // Testimonials methods
    addTestimonial() {
      this.testimonials.push({
        name: "",
        role: "",
        text: "",
        imageUrl: "",
        uploadType: "url",
      });
    },
    removeTestimonial(index: number) {
      this.testimonials.splice(index, 1);
    },
    handleTestimonialImageChange(event: Event, index: number) {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        const file = target.files[0];

        // Validate file type
        const allowedTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"];
        if (!allowedTypes.includes(file.type)) {
          this.error = "Tipo de archivo no válido. Solo se permiten imágenes.";
          target.value = "";
          return;
        }

        // Validate file size (5MB max for testimonials)
        if (file.size > 5 * 1024 * 1024) {
          this.error = "El archivo es demasiado grande. Tamaño máximo: 5MB";
          target.value = "";
          return;
        }

        // Store file and create preview
        const testimonial = this.testimonials[index];
        if (testimonial) {
          testimonial.imageFile = file;
          const reader = new FileReader();
          reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target?.result && testimonial) {
              testimonial.imageUrl = e.target.result as string;
            }
          };
          reader.readAsDataURL(file);
        }
        this.error = "";
      }
    },

    // How It Works methods
    addStep() {
      const nextNum = this.howItWorksSteps.length + 1;
      this.howItWorksSteps.push({ title: `${nextNum}. `, description: "" });
    },
    removeStep(index: number) {
      this.howItWorksSteps.splice(index, 1);
    },

    // Team Members methods
    addTeamMember() {
      this.teamMembers.push({ name: "", role: "", imageUrl: "", uploadType: "url" });
    },
    removeTeamMember(index: number) {
      this.teamMembers.splice(index, 1);
    },
    handleTeamMemberImageChange(event: Event, index: number) {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        const file = target.files[0];

        // Validate file type
        const allowedTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"];
        if (!allowedTypes.includes(file.type)) {
          this.error = "Tipo de archivo no válido. Solo se permiten imágenes.";
          target.value = "";
          return;
        }

        // Validate file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
          this.error = "El archivo es demasiado grande. Tamaño máximo: 5MB";
          target.value = "";
          return;
        }

        // Store file and create preview
        const member = this.teamMembers[index];
        if (member) {
          member.imageFile = file;
          const reader = new FileReader();
          reader.onload = (e: ProgressEvent<FileReader>) => {
            if (e.target?.result && member) {
              member.imageUrl = e.target.result as string;
            }
          };
          reader.readAsDataURL(file);
        }
        this.error = "";
      }
    },

    loadExample(type: string) {
      switch (type) {
        case "info_items":
          this.infoItems = [
            {
              icon: "bi-lightbulb",
              title: "Iniciativa",
              description:
                "Descubrí oportunidades únicas para generar un impacto positivo en tu comunidad universitaria.",
            },
            {
              icon: "bi-trophy",
              title: "Objetivos",
              description: "Alcanzá tus metas personales y profesionales mientras ayudás a otros.",
            },
            {
              icon: "bi-flag",
              title: "Misión",
              description:
                "Conectar estudiantes comprometidos con organizaciones que necesitan su talento.",
            },
            {
              icon: "bi-people",
              title: "Para los Estudiantes",
              description:
                "Accedé a una amplia variedad de oportunidades diseñadas para estudiantes.",
            },
          ];
          break;
        case "testimonials":
          this.testimonials = [
            {
              name: "María González",
              role: "Estudiante de Medicina",
              text: "Participar en este voluntariado cambió mi perspectiva sobre el servicio comunitario. Una experiencia inolvidable.",
              imageUrl: "https://via.placeholder.com/80",
            },
            {
              name: "Juan Pérez",
              role: "Estudiante de Ingeniería",
              text: "Aprendí mucho trabajando con la comunidad. Definitivamente lo recomiendo.",
              imageUrl: "https://via.placeholder.com/80",
            },
            {
              name: "Ana Martínez",
              role: "Estudiante de Derecho",
              text: "Una oportunidad única para aplicar mis conocimientos y ayudar a otros.",
            },
          ];
          break;
        case "how_it_works_steps":
          this.howItWorksSteps = [
            {
              title: "1. Registrate",
              description:
                "Creá tu cuenta en el sistema con tu email universitario y completá tu perfil.",
            },
            {
              title: "2. Explorá Oportunidades",
              description:
                "Navegá por los diferentes voluntariados disponibles y encontrá el que más te interese.",
            },
            {
              title: "3. Inscribite",
              description: "Aplicá a los voluntariados que te interesen y esperá la confirmación.",
            },
            {
              title: "4. Participá",
              description: "Asistí a las actividades programadas y registrá tu participación.",
            },
            {
              title: "5. Capacitate",
              description: "Participá en las capacitaciones relacionadas a tu voluntariado.",
            },
            {
              title: "6. Obtené tu Certificado",
              description:
                "Al completar el voluntariado, recibí tu certificado oficial de participación.",
            },
          ];
          break;
        case "team_members":
          this.teamMembers = [
            {
              name: "Dr. Juan Pérez",
              role: "Director de Voluntariado",
              imageUrl: "https://via.placeholder.com/150",
            },
            {
              name: "Lic. María González",
              role: "Coordinadora General",
              imageUrl: "https://via.placeholder.com/150",
            },
            {
              name: "Carlos Rodríguez",
              role: "Coordinador de Proyectos",
            },
            {
              name: "Ana Martínez",
              role: "Administradora",
            },
          ];
          break;
      }
    },
  },
});
</script>

<style scoped>
.landing-config-admin {
  min-height: 100vh;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  border-radius: 0.375rem;
  border: 1px solid #dee2e6;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.text-primary {
  color: #0d6efd !important;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.alert {
  border-radius: 0.375rem;
}

.border-top {
  border-top: 1px solid #dee2e6 !important;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.preview-section {
  background-color: #f8f9fa;
  border-radius: 0.375rem;
  padding: 1rem;
}

/* Dynamic Content Styles */
.dynamic-content-header .alert {
  background-color: #e7f3ff;
  border-color: #b3d9ff;
  color: #004085;
}

/* Configuration Section Card Styles (for Basic Info, Contact, Footer) */
.config-section-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.config-section-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.config-section-header {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s ease;
}

.config-section-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.config-section-header h5 {
  font-weight: 600;
  color: #495057;
  margin: 0;
  font-size: 1.1rem;
}

.config-section-header i.bi-chevron-up,
.config-section-header i.bi-chevron-down {
  font-size: 1.3rem;
  color: #6c757d;
  transition: transform 0.3s ease;
}

.config-section-body {
  padding: 1.75rem 1.5rem;
  animation: slideDown 0.3s ease;
}

/* Image Preview Styles */
.image-preview-container {
  border: 2px dashed #dee2e6;
  border-radius: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

.image-preview-container:hover {
  border-color: #0d6efd;
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.image-preview {
  max-width: 100%;
  max-height: 300px;
  border-radius: 0.375rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.image-preview:hover {
  transform: scale(1.02);
}

.dynamic-field-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
}

.dynamic-field-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.dynamic-field-header {
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s ease;
}

.dynamic-field-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.dynamic-field-header h6 {
  font-weight: 600;
  color: #495057;
  margin: 0;
}

.dynamic-field-header i.bi-chevron-up,
.dynamic-field-header i.bi-chevron-down {
  font-size: 1.2rem;
  color: #6c757d;
  transition: transform 0.3s ease;
}

.dynamic-field-body {
  padding: 1.5rem 1.25rem;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.json-editor {
  font-size: 0.875rem;
  line-height: 1.6;
  background-color: #f8f9fa;
  border: 2px solid #dee2e6;
  transition: all 0.2s ease;
}

.json-editor:focus {
  background-color: #ffffff;
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
}

.json-editor.is-invalid {
  border-color: #dc3545;
  background-color: #fff5f5;
}

.json-editor.is-invalid:focus {
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.15);
}

.json-help-text {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #198754;
  display: flex;
  align-items: center;
}

.invalid-feedback {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.btn-outline-secondary {
  border-color: #6c757d;
  color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}

/* Form Item Card Styles */
.form-item-card {
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  transition: all 0.3s ease;
  position: relative;
}

.form-item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #0d6efd;
}

.form-item-card h6 {
  font-weight: 600;
  color: #495057;
}

.form-item-card .btn-outline-danger {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

/* Icon Selector Styles */
.icon-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.15s ease-in-out;
}

.icon-select:hover {
  border-color: #0d6efd;
}

.icon-select:focus {
  outline: none;
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Icon Preview Styles */
.icon-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 0.375rem;
  margin: 0.75rem 0;
  min-height: 100px;
  border: 2px dashed #dee2e6;
  transition: all 0.3s ease;
}

.icon-preview:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  border-color: #0d6efd;
}

.icon-preview-large {
  font-size: 3rem;
  color: #0d6efd;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Button Styles */
.btn-outline-primary {
  border: 2px solid #0d6efd;
  color: #0d6efd;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(13, 110, 253, 0.3);
}

/* Radio Button Group Styles */
.btn-group .btn-check:checked + .btn-outline-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
}

.btn-group .btn-outline-primary {
  border-width: 1px;
  font-weight: 500;
}

.btn-group .btn-outline-primary:not(:checked) {
  transform: none;
  box-shadow: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dynamic-field-header {
    padding: 0.875rem 1rem;
  }

  .dynamic-field-body {
    padding: 1rem;
  }

  .json-editor {
    font-size: 0.8rem;
  }

  .form-item-card {
    padding: 1rem;
  }

  .icon-preview-large {
    font-size: 2.5rem;
  }
}
</style>
