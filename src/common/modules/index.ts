export * from "./swagger.module";
export * from "./config.module";
export * from "./mongoose.module";
export * from "./jwt.module";

import { ConfigModule } from "./config.module";
import { JwtModule } from "./jwt.module";
import { MongooseModule } from "./mongoose.module";

export const EssentialModules = [ConfigModule, JwtModule, MongooseModule];
