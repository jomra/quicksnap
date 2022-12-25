import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://dtjbbjbsxwzpwcsxepgi.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0amJiamJzeHd6cHdjc3hlcGdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzE0MDU1NjQsImV4cCI6MTk4Njk4MTU2NH0.-fvkD4W5W9vKZ03ONeWEk91hS6bKwrq0C1cgfMortS8';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)