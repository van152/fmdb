char __fastcall sub_140E72100(__int64 a1, __int16 a2)
{
  __int64 v3; // rdx
  char result; // al
  __int64 v5; // rcx
  __int64 v6; // rdi
  char v7; // al
  char v8; // cl
  float v9; // xmm0_4
  int v10; // eax
  int v11; // edx
  float v12; // xmm1_4

  v3 = *(_QWORD *)(a1 + 216);
  result = 6;
  if ( v3 != 0 && (*(_BYTE *)(a1 + 185) != 0 && (v5 = *(_QWORD *)(v3 + 272)) != 0 || (v5 = *(_QWORD *)(v3 + 264)) != 0) )
  {
    v6 = *(_QWORD *)(*(_QWORD *)(v5 + 368) + 240LL);
    if ( v6 != 0 )
    {
      v7 = sub_141758D10();
      v8 = 1;
      if ( v7 >= 2 )
        v8 = v7;
      v9 = *(float *)(v6 + 228) - (float)(MEMORY[0x1417597F0] - *(float *)(v6 + 228));
      v10 = *(_DWORD *)(v6 + 12);
      if ( v10 == 3 )
      {
        v11 = (int)(float)(MEMORY[0x141871408] * v9);
      }
      else
      {
        v9 = v9 * MEMORY[0x141774724];
        if ( v10 == 5 )
          v9 = v9 * MEMORY[0x141879578];
        v11 = (int)(float)(MEMORY[0x141871408] * v9);
        switch ( v10 )
        {
          case 2:
            LOWORD(v11) = 5500;
            break;
          case 4:
            LOWORD(v11) = 6600;
            break;
          case 5:
            LOWORD(v11) = 2700;
            break;
          case 6:
            LOWORD(v11) = 6000;
            break;
          default:
            break;
        }
      }
      result = 1;
      if ( a2 <= 8249 )
      {
        result = 2;
        if ( (__int16)v11 > a2 )
        {
          v12 = (float)v8 / MEMORY[0x141775564];
          result = 3;
          if ( (__int16)(int)(float)((float)(MEMORY[0x1417D40F4] * v9) * v12) > a2 )
          {
            result = 4;
            if ( (__int16)(int)(float)((float)(MEMORY[0x141876F68] * v9) * v12) > a2 )
              return ((__int16)(int)(float)(v12 * (float)(v9 * MEMORY[0x141876F6C])) > a2) + 5;
          }
        }
      }
    }
  }
  return result;
}
