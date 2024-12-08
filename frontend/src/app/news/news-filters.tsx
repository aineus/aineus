import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface NewsFiltersProps {
  filters: {
    category: string;
    timeFrame: string;
  };
  onChange: (filters: any) => void;
}

const CATEGORIES = [
  { id: 'all', label: 'All' },
  { id: 'technology', label: 'Technology' },
  { id: 'business', label: 'Business' },
  { id: 'politics', label: 'Politics' },
  { id: 'science', label: 'Science' },
];

const TIME_FRAMES = [
  { id: '24h', label: 'Last 24 Hours' },
  { id: '7d', label: 'Last 7 Days' },
  { id: '30d', label: 'Last 30 Days' },
];

export function NewsFilters({ filters, onChange }: NewsFiltersProps) {
  return (
    <Card className="p-4">
      <div className="space-y-4">
        <div>
          <h3 className="text-sm font-medium mb-2">Categories</h3>
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((category) => (
              <Button
                key={category.id}
                variant={filters.category === category.id ? "default" : "outline"}
                size="sm"
                onClick={() => onChange({ ...filters, category: category.id })}
              >
                {category.label}
              </Button>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium mb-2">Time Frame</h3>
          <div className="flex flex-wrap gap-2">
            {TIME_FRAMES.map((timeFrame) => (
              <Button
                key={timeFrame.id}
                variant={filters.timeFrame === timeFrame.id ? "default" : "outline"}
                size="sm"
                onClick={() => onChange({ ...filters, timeFrame: timeFrame.id })}
              >
                {timeFrame.label}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}