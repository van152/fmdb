void __fastcall sub_143C39AF0(__int64 a1, __int64 a2)
{
  __int64 v3; // rbx
  int v4; // r14d
  __int64 v5; // rsi
  __int64 *v6; // rax
  float v7; // xmm6_4
  __int64 v8; // rax
  char v9; // al
  int v10; // ecx
  int v11; // eax
  int v12; // r8d
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rdi
  __int64 v16; // rcx
  unsigned __int8 v17; // al
  __int64 v18; // rcx

  if ( a2 != 0 )
  {
    v3 = *(_QWORD *)(a1 + 216);
    if ( v3 != 0 )
    {
      if ( (v4 = a2, *(_BYTE *)(a1 + 185) != 0) && (v5 = *(_QWORD *)(v3 + 272)) != 0
        || (v5 = *(_QWORD *)(v3 + 264)) != 0 )
      {
        v6 = *(__int64 **)(a1 + 24);
        v7 = MEMORY[0x14187CB98];
        if ( v6 != *(__int64 **)(a1 + 32) )
        {
          v8 = *v6;
          if ( v8 != 0 )
            v7 = (float)(__int16)(int)((double)*(__int16 *)(v8 + 168) * MEMORY[0x141764698]);
        }
        v9 = sub_141758D10();
        v10 = 1;
        if ( v9 < 2 )
          v9 = 1;
        v11 = (int)(float)((float)(v7 / (float)(__int16)(500 * (unsigned __int8)v9)) * MEMORY[0x141784F6C]);
        if ( v11 >= 2 )
          v10 = v11;
        v12 = 100;
        if ( v10 < 100 )
          v12 = v10;
        sub_1413FB4C0(v4, v3, v12, 0, a1, 0);
        if ( ((*(__int64 (__fastcall **)(__int64, __int64, _QWORD))(*(_QWORD *)qword_141B5EDE8 + 40LL))(
                qword_141B5EDE8,
                a1,
                0)
            & 0xFE) == 6 )
        {
          v13 = *(_QWORD *)(v5 + 248) - *(_QWORD *)(v5 + 240);
          if ( v13 != 0 )
          {
            v14 = v13 >> 4;
            v15 = 8;
            do
            {
              v16 = *(_QWORD *)(v5 + 240);
              v17 = *(_BYTE *)(v16 + v15 - 8);
              if ( v17 <= 0xFDu )
              {
                v18 = *(_QWORD *)(v16 + v15);
                if ( v18 != 0 )
                  sub_1413FB4C0(v4, *(_QWORD *)(v18 + 368), 5 * v17, 0, a1, 0);
              }
              v15 += 16;
              --v14;
            }
            while ( v14 != 0 );
          }
        }
      }
    }
  }
}
