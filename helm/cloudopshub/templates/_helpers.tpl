{{- define "cloudopshub.name" -}}
{{- .Chart.Name -}}
{{- end }}

{{- define "cloudopshub.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}
