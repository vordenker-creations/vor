# Frontend Architecture Handbook: Tech Job Board Dashboard (Next.js 15 & TailwindCSS)

Tài liệu này đóng vai trò là bản thiết kế hệ thống (System Design Blueprint) và Hướng dẫn Phong cách Thiết kế (Design & Style Guide) cho ứng dụng Đăng tin tuyển dụng dành riêng cho Web Developer/Ngành Công nghệ. Thiết kế mang phong cách Modern SaaS / AI Startup với trải nghiệm chuyển động mượt mà (smooth motion) và kính mờ (glassmorphism).

---

## 1. Cấu trúc thư mục dự án (Folder Structure)

Dưới đây là sơ đồ cấu trúc thư mục tối ưu cho dự án chạy Next.js 15 (App Router), TypeScript, TailwindCSS, shadcn/ui và Zustand:

```text
├── public/                  # Các tài nguyên tĩnh (logos, minimal illustrations)
├── src/
│   ├── app/                 # Next.js 15 App Router Layout & Pages
│   │   ├── layout.tsx       # Root Layout (Fonts, Global CSS, Providers)
│   │   ├── page.tsx         # Trang chủ + Danh sách công việc (Job Board Hero + List)
│   │   ├── login/           # Trang Đăng nhập
│   │   │   └── page.tsx
│   │   ├── register/        # Trang Đăng ký
│   │   │   └── page.tsx
│   │   ├── jobs/
│   │   │   ├── post/        # Trang Đăng tin tuyển dụng (Post Job Form)
│   │   │   │   └── page.tsx
│   │   │   └── [id]/        # Trang Chi tiết bài tuyển dụng (Job Details)
│   │   │       └── page.tsx
│   │   └── profile/         # Trang Hồ sơ cá nhân (Profile Page)
│   │       └── page.tsx
│   │
│   ├── components/          # Reusable Components (Thành phần tái sử dụng)
│   │   ├── ui/              # shadcn/ui components (được custom lại style)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── textarea.tsx
│   │   │   ├── label.tsx
│   │   │   └── dialog.tsx
│   │   ├── shared/          # Các layout dùng chung
│   │   │   ├── navbar.tsx   # Sticky glassmorphic navbar
│   │   │   └── footer.tsx
│   │   └── jobs/            # Các component dành riêng cho module Jobs
│   │       ├── job-card.tsx # Thẻ công việc (Job card) có hover lift
│   │       └── job-list.tsx # Bộ lọc kết hợp list bài viết
│   │
│   ├── hooks/               # Custom React Hooks
│   ├── lib/                 # Utility functions & Third-party configs
│   │   ├── utils.ts         # Hàm hỗ trợ class merging (clsx + tailwind-merge)
│   │   └── validation.ts    # Zod schemas cho Auth & Post Job
│   │
│   ├── store/               # Zustand state management
│   │   └── useAuthStore.ts  # Quản lý trạng thái đăng nhập, profile
│   │
│   └── styles/
│       └── globals.css      # Custom CSS variables, gradients và class nền
├── tailwind.config.ts       # Cấu hình Tailwind hệ thống
├── tsconfig.json            # Cấu hình TypeScript
└── package.json
```

---

## 2. Kiến trúc Thành phần (Component Architecture)

Hệ thống Component được phân chia rõ ràng để đảm bảo tính module và khả năng bảo trì:
*   **Atomic UI (Thư mục `components/ui/`):** Các nguyên tử UI gốc (button, input, badge, dialog). Không chứa logic nghiệp vụ, hoàn toàn styled bằng Tailwind CSS variables.
*   **Feature Components (Thư mục `components/jobs/`):** Nhận props để hiển thị thông tin nghiệp vụ cụ thể. Ví dụ: `JobCard` nhận object Job, thực hiện hiển thị tag kỹ năng và trạng thái.
*   **Global Layout Layouts (Thư mục `components/shared/`):** Quản lý layout cấu trúc khung của trang như `Navbar` điều hướng, xử lý hiển thị Avatar khi user đã đăng nhập, liên kết Đăng ký/Đăng nhập.
*   **Page Container (`src/app/`):** Nơi tích hợp dữ liệu, quản lý route và kết nối với Zustand store để kiểm soát view state.

---

## 3. Hệ thống Thiết kế (Design System & Color Tokens)

Sử dụng bảng màu sâu sắc kiểu AI/Tech/SaaS với sự tương phản cao và hiệu ứng kính mờ (Glassmorphic):

### Color Tokens (CSS Variables - `globals.css`)
```css
:root {
  /* Nền tối chủ đạo với sắc xanh dương thẳm */
  --background: 224 71% 4%;     /* #030712 - Cực tối */
  --foreground: 210 40% 98%;    /* #F8FAFC - Off white */

  /* Màu Card & Panel (Hiệu ứng kính mờ - Glassmorphic) */
  --card: 222 47% 7%;           /* #0A0F24 */
  --card-foreground: 210 40% 98%;
  --card-border: 217 32% 17%;   /* #1E293B */

  /* Màu thương hiệu & Accent */
  --primary: 188 86% 53%;       /* #22D3EE - Cyan Accent */
  --primary-foreground: 224 71% 4%;
  
  --secondary: 217 32% 17%;     /* Deep Navy Slate */
  --secondary-foreground: 210 40% 98%;

  /* Trạng thái đặc biệt */
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  
  --accent: 188 86% 53% 0.15;   /* Light Cyan overlay */
  --accent-foreground: 188 86% 53%;

  --destructive: 0 84.2% 60.2%; /* Đỏ ruby dịu mắt */
  --destructive-foreground: 210 40% 98%;

  --border: 217 32% 17%;
  --input: 217 32% 17%;
  --ring: 188 86% 53% 0.5;      /* Ring glow khi focus */

  --radius: 1rem;               /* Rounded corners lớn cho card (16px) */
}
```

### Tailwind Configuration (`tailwind.config.ts`)
```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        border: "hsl(var(--border))",
        ring: "var(--ring)",
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      boxShadow: {
        'glow-primary': '0 0 15px rgba(34, 211, 238, 0.35)',
        'glow-hover': '0 0 25px rgba(34, 211, 238, 0.5)',
        'glass-shadow': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      backdropBlur: {
        xs: '2px',
        glass: '12px',
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
}
export default config
```

---

## 4. Nguyên tắc Chuyển động (Animation Guidelines)

*Chỉ sử dụng Framer Motion cho animation. Áp dụng chuyển động mượt mà dưới 300ms, không lag layout:*
*   **Trang Thái Hover:**
    *   *Buttons:* Nút Primary sẽ có hiệu ứng `scale: 1.02` kèm tăng độ sáng shadow glow.
    *   *Job Cards:* Di chuyển lên (`y: -4px`), viền đổi sang màu Primary nhẹ (`border-color: rgba(34, 211, 238, 0.4)`), bóng đổ chuyển từ `shadow-md` sang `shadow-glass-shadow`.
*   **Chuyển Trang (Page Transitions):**
    *   Wrap các trang trong thẻ `<motion.div>` của Framer Motion với transition dạng Fade-In mượt:
        ```typescript
        const pageTransition = {
          initial: { opacity: 0, y: 10 },
          animate: { opacity: 1, y: 0 },
          exit: { opacity: 0, y: -10 },
          transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] } // Easing professional
        }
        ```
*   **Phản hồi Input Focus:**
    *   Khi trỏ chuột vào input, outline sẽ phát sáng (ring-glow-primary) nhờ transition CSS (duration-300).

---

## 5. Chiến lược Responsive & Typography Scale

### Typography System
*   **Font chữ:** `Plus Jakarta Sans` hoặc `Inter` làm font chữ chủ đạo, tối ưu hiển thị chữ công nghệ.
*   **Tỷ lệ cỡ chữ (Scale):**
    *   *Hero Heading:* `text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight`
    *   *Section Heading:* `text-2xl md:text-3xl font-bold tracking-tight`
    *   *Job Title (Card):* `text-lg md:text-xl font-semibold`
    *   *Body text:* `text-sm md:text-base text-slate-300 leading-relaxed`
    *   *Muted / Meta data:* `text-xs text-slate-400 font-medium`

### Responsive Strategy
*   **Mobile (<640px):** Navbar thu gọn bằng icon Menu Drawer, Grid xếp dọc 1 cột hoàn toàn, giảm padding của panel xuống `p-4`.
*   **Tablet (640px - 1024px):** Grid 2 cột cho danh sách tin tuyển dụng, Form hiển thị 1 cột lớn căn giữa.
*   **Desktop (>1024px) & Ultra wide:** Grid 3 cột cho danh sách tin, Sidebar mỏng ở chi tiết công việc, layout cân bằng đối xứng tối đa.

---

## 6. Quy tắc UI Component & Thực tiễn UX tốt nhất (UX Best Practices)

1.  **Phân biệt Màu Nút (Buttons):**
    *   *Primary Button (Nút hành động chính - Đăng tin, Apply):* Màu nền Cyan, text Dark Blue, có shadow glow nhẹ.
    *   *Secondary Button (Nút bộ lọc, xem thêm):* Border mảnh, nền bán trong suốt, text trắng.
    *   *Danger Button (Hủy, xóa tin):* Nền Đỏ ruby đậm nhạt, text trắng, không bóng sáng cyan.
    *   *Ghost Button (Đăng nhập, Back):* Không nền, text xám/trắng, xuất hiện nền nhẹ khi hover.
2.  **Trạng thái Form chặt chẽ:**
    *   Focus: Input viền Primary Cyan kèm ring glow.
    *   Error: Thêm viền đỏ nhạt và text lỗi màu đỏ chân thật dưới ô input. Cần hiển thị lỗi ngay khi user rời focus (onBlur).
    *   Disabled: Độ mờ `opacity-50`, `pointer-events-none`.
3.  **Realtime Validation:**
    *   Sử dụng Zod và React Hook Form cho tất cả biểu mẫu. Ví dụ: Password khi đăng ký phải có tối thiểu 8 ký tự, email đúng format.

---

## 7. Các Section Chi Tiết Theo Trang

### 1. Navbar
*   Sticky trên cùng, `backdrop-filter: blur(12px)` kết hợp màu nền `bg-background/80`.
*   Đường viền dưới siêu mảnh (`border-b border-border/40`).
*   Logo chữ tối giản kèm biểu tượng dạng tinh tú (✦ DevHire).
*   Góc phải: Nút "Post a Job" phát sáng nhẹ và Avatar tròn dẫn tới Profile.

### 2. Hero Section
*   Một khối lớn nền chuyển sắc Blue-to-Dark mượt, bo góc tròn lớn `rounded-3xl` bóng bẩy.
*   Tiêu đề cực lớn: "Find Your Dream Developer Role" & "Build the Future".
*   Search Bar tích hợp trực tiếp ngay trong Hero với thiết kế mờ ảo (Glassmorphism), cho phép lọc kỹ năng nhanh.

### 3. Job Card & Detail Page
*   Card hiển thị tên Job, Company (có logo tròn nhỏ), mức lương dạng tag nổi bật (`$120k - $150k`), Location và danh sách Badge kỹ năng (`React`, `NodeJS`, `Next.js`).
*   Khi nhấn vào Card, ứng dụng sẽ mở một modal chi tiết hoặc chuyển tiếp sang trang chi tiết với bố cục chia đôi (bên trái là mô tả Rich Text, bên phải là thông tin Apply nhanh).

### 4. Post Job Form
*   Phần Đăng bài chia làm 3 cụm thông tin:
    *   `1. Thông tin Công ty` (Name, Website, Logo)
    *   `2. Chi tiết Công việc` (Title, Role, Location, Salary Range)
    *   `3. Yêu cầu kỹ năng & Mô tả chi tiết` (Rich Text area + tags input).
*   Giao diện nhập tối giản với khoảng cách rộng rãi, chống quá tải thông tin.

---

## 8. Prompt Code Generation Chuẩn Production

*Hãy copy và sử dụng prompt dưới đây cho các công cụ AI code generation để tạo code Next.js 15 khớp 100% với thiết kế:*

```text
Act as a Senior Frontend Architect and UI/UX Specialist. Write a production-grade, highly polished, interactive code snippet using Next.js 15 (App Router), React, TypeScript, TailwindCSS, Framer Motion, and Lucide React.

The site is a premium, minimalist Developer Job Board. Apply a dark theme with the following specifications:
- Theme: Navy Blue background (#030712), Glassmorphic cards (#0A0F24 with border #1E293B and backrop-blur).
- Primary Accent: Cyan (#22D3EE) for primary CTA glow buttons, highlights, and active focus rings.
- Styling: Soft drop shadows, large rounded corners (rounded-2xl to rounded-3xl), clean spacing, professional typography (Inter / Plus Jakarta Sans).
- Component separation: Clean layouts, consistent grid margins, explicit paddings (p-6 to p-8 for cards).

Create a single-file showcase or highly structured component files covering:
1. A sticky glassmorphic navbar with logo, menu links, and login state.
2. A hero card with gradient background, tech illustration, and quick search.
3. Job card component with lift-on-hover animation (y: -4px), displaying: Title, Company, Tech Tags (Badges), Salary Badge, and an Apply CTA.
4. An interactive Post Job Form split into sections (Company Info, Job Spec, Rich Requirements) with glowing focus inputs and error states.
5. An interactive Login/Register card with realtime validation styling.
6. A responsive Profile page showing avatar card, biography, skill badges, and active postings list.

Ensure the code has:
- No visual glitches or overlaps.
- High-contrast colors for text readability.
- Frame Motion animations under 300ms using realistic physics transitions (spring or ease-out).
- Responsive grid structure (1 col on mobile, 2 on tablet, 3 on desktop).
- No mock/placeholder libraries. Render beautiful SVGs for illustrations.
```
