// Student API: Get own info, enrollments, subjects, questions, evaluations
import api from './client'
import type {
  UserResponse,
  EnrollmentResponse,
  SubjectResponse,
  QuestionResponse,
  TAEvaluationResponse,
} from '../types/api'

// Get own user info
export const getMe = async (): Promise<UserResponse> => (await api.get('/user/me')).data

// Get own enrollments
export const getEnrollments = async (): Promise<EnrollmentResponse[]> =>
  (await api.get('/student/enrollments')).data

// Get subjects from own enrollments
export const getSubjects = async (): Promise<SubjectResponse[]> =>
  (await api.get('/student/subjects')).data

// Get questions from enrolled subjects
export const getQuestions = async (): Promise<QuestionResponse[]> =>
  (await api.get('/student/questions')).data

// Get own evaluations (read-only)
export const getEvaluations = async (): Promise<TAEvaluationResponse[]> =>
  (await api.get('/student/evaluations')).data
