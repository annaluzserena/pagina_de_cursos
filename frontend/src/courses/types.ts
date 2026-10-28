export interface Course {
  id: string
  title: string
  topic: string
  category_id: string
  source_url: string
  provider: string | null
  version: string
  edition_year: number
  instructors: string
  has_quizzes: boolean
  requires_exam: boolean
  offers_certificate: boolean
  is_endorsed: boolean
  endorsing_organization: string | null
}
