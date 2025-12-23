/**
 * Home Page Component
 */

const HomePage = ({ onNavigate }) => {
    const menuItems = [
        {
            id: 'education',
            title: 'آموزش بیمار',
            description: 'دریافت ویدیوهای آموزشی',
            icon: Icons.Camera,
            color: 'blue'
        },
        {
            id: 'symptoms',
            title: 'ثبت علائم',
            description: 'پیگیری قند، فشار و وزن',
            icon: Icons.Activity,
            color: 'green'
        },
        {
            id: 'contact',
            title: 'ارتباط با کارشناس',
            description: 'اطلاعات تماس',
            icon: Icons.Phone,
            color: 'orange'
        },
        {
            id: 'support',
            title: 'پشتیبانی',
            description: 'ارتباط از طریق ایتا',
            icon: Icons.HelpCircle,
            color: 'purple',
            action: () => window.open(CONFIG.CONTACT.eitaa, '_blank')
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 p-4 md:p-8">
            <div className="max-w-6xl mx-auto">
                <h1 className="text-3xl md:text-4xl font-bold text-center text-blue-900 mb-8 md:mb-12">
                    سامانه آموزش و پیگیری سلامت
                </h1>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
                    {menuItems.map(item => (
                        <div
                            key={item.id}
                            onClick={() => item.action ? item.action() : onNavigate(item.id)}
                            className={`bg-white rounded-3xl p-6 md:p-8 shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105 border-2 border-${item.color}-200`}
                        >
                            <div className="flex flex-col items-center text-center">
                                <div className={`bg-${item.color}-100 p-4 md:p-6 rounded-full mb-4 text-${item.color}-600`}>
                                    <item.icon />
                                </div>
                                <h2 className={`text-xl md:text-2xl font-bold text-${item.color}-900 mb-2`}>
                                    {item.title}
                                </h2>
                                <p className="text-gray-600">{item.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HomePage;
                          }
