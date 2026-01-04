// TA API: List students, enrollments, subjects, questions; CRUD own evaluations
import api from './client'
import type {
  UserResponse,
  EnrollmentResponse,
  SubjectResponse,
  QuestionResponse,
  TAEvaluationCreate,
  TAEvaluationResponse,
  TAEvaluationUpdate,
} from '../types/api'

// List students (students only, exclude admins/TAs)
export const getStudents = async (): Promise<UserResponse[]> => (await api.get('/ta/students')).data

// List enrollments
export const getEnrollments = async (): Promise<EnrollmentResponse[]> =>
  (await api.get('/ta/enrollments')).data

// List subjects
export const getSubjects = async (): Promise<SubjectResponse[]> =>
  (await api.get('/ta/subjects')).data

// List questions
export const getQuestions = async (): Promise<QuestionResponse[]> =>
  (await api.get('/ta/questions')).data

// List evaluations
export const getEvaluations = async (): Promise<TAEvaluationResponse[]> =>
  (await api.get('/ta/evaluations')).data

// Create evaluation (self only)
export const createEvaluation = async (body: TAEvaluationCreate) =>
  (await api.post('/ta/evaluations', body)).data

// Update evaluation (self only)
export const updateEvaluation = async (id: number, body: TAEvaluationUpdate) =>
  (await api.put(`/ta/evaluations/${id}`, body)).data

// Delete evaluation (self only)
export const deleteEvaluation = async (id: number) =>
  (await api.delete(`/ta/evaluations/${id}`)).data
