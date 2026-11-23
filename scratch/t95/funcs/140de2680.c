unsigned __int8 __fastcall sub_140DE2680(__int64 a1, int a2)
{
  __int64 v3; // rcx
  unsigned __int8 result; // al
  __int64 *v6; // rax
  __int64 v7; // rax
  char v8; // cl
  __int64 v9; // rax
  __int64 v10; // rsi
  unsigned int v11; // edx
  int v12; // ebx
  unsigned __int64 v13; // rdx
  __int64 v14; // rbx
  unsigned __int64 v15; // rdx
  __int64 v16; // rbx
  __int64 v17; // rdi
  __int64 v18; // r8
  unsigned int v19; // ecx
  char v20; // bl
  float v21; // xmm0_4
  unsigned int v22; // edi
  unsigned int v23; // ecx

  v3 = *(_QWORD *)(a1 - 176);
  if ( v3 != 0 )
    return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 80LL))(v3);
  v6 = *(__int64 **)(a1 - 168);
  if ( v6 != nullptr )
  {
    v3 = *v6;
    if ( *v6 != 0 )
      return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v3 + 80LL))(v3);
  }
  if ( a2 != 0 )
  {
    v7 = *(int *)(*(_QWORD *)(a1 - 328) + 4LL);
    v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v7 - 328) + 1304LL))(v7 + a1 - 336 + 8);
    result = 1;
    if ( v8 == 0 )
      return result;
    v9 = *(int *)(*(_QWORD *)(a1 - 328) + 4LL);
    v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v9 - 328) + 1696LL))(v9 + a1 - 336 + 8);
    if ( (a2 | 2) == 3 && *(_QWORD *)(v10 + 96) != 0 )
    {
      result = *(_BYTE *)(v10 + 218);
      if ( a2 == 1 )
      {
        v11 = result & 0xFE;
        if ( v11 > 0x18 || (v12 = 16777296, !_bittest(&v12, v11)) )
        {
          if ( v11 != 70 && v11 != 84 )
          {
            v13 = (unsigned int)result - 8;
            if ( (unsigned int)v13 > 0x3B || (v14 = 0xC00000000000003LL, !_bittest64(&v14, v13)) )
            {
              if ( (result & 0xF6) != 0x26 )
              {
                v15 = (unsigned int)result - 28;
                if ( (unsigned int)v15 > 0x35 || (v16 = 0x30030000000003LL, !_bittest64(&v16, v15)) )
                {
                  if ( result != 0 )
                    return result;
                }
              }
            }
          }
        }
      }
      else if ( result != 0 )
      {
        return result;
      }
    }
    v17 = *(_QWORD *)(a1 - 120);
    if ( v17 != 0 )
    {
      LOBYTE(v18) = (unsigned __int8)sub_140086FF0() != 0;
      result = sub_1413FFD00(v17, 0, v18);
      if ( v10 != 0 && (result & 0xFE) != 0x3E && ((result & 0xFE) == 58 || (result & 0xFC) == 60) )
      {
        v19 = ((unsigned int)(26215 * *(char *)(v10 + 52) + 52430) >> 31)
            + ((26215 * *(char *)(v10 + 52) + 52430) >> 17);
        if ( (__int16)(((unsigned int)(26215 * *(char *)(v10 + 52) + 52430) >> 31)
                     + ((26215 * *(char *)(v10 + 52) + 52430) >> 17)) < 2 )
          LOWORD(v19) = 1;
        v20 = 20;
        if ( (unsigned __int16)v19 >= 0x14u )
          LOBYTE(v19) = 20;
        v21 = (float)(char)v19;
        v22 = (unsigned int)(26215 * *(char *)(v10 + 57) + 52430) >> 31;
        v23 = v22 + ((26215 * *(char *)(v10 + 57) + 52430) >> 17);
        if ( (__int16)(v22 + ((26215 * *(char *)(v10 + 57) + 52430) >> 17)) < 2 )
          LOWORD(v23) = 1;
        if ( (unsigned __int16)v23 < 0x14u )
          v20 = v23;
        if ( (float)(v21 / (float)v20) >= MEMORY[0x141876F40] )
          return 58;
      }
      return result;
    }
  }
  return 0;
}
