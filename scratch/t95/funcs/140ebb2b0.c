// THUNK ALIAS -> sub_143C93DF0 (jmp:0x140ebb2b0->0x143c93df0)
__int64 __fastcall sub_143C93DF0(__int64 a1, char *a2, _BYTE *a3)
{
  __int64 result; // rax
  int v6; // ebx
  __int64 v7; // rdx
  int v8; // ecx
  int v9; // eax
  unsigned int v10; // ecx
  int v11; // r8d
  int v12; // ebx
  unsigned int v13; // edx
  unsigned __int8 v14; // bl
  char v15; // bl
  unsigned int v16; // ebx

  result = *(_QWORD *)(a1 + 96);
  if ( result != 0 )
  {
    if ( (v6 = a1, *(_BYTE *)(a1 + 245) != 0) && (v7 = *(_QWORD *)(result + 272)) != 0
      || (v7 = *(_QWORD *)(result + 264)) != 0 )
    {
      result = sub_1408B4CB0(qword_141B5AD60, *(_QWORD *)(v7 + 368), *(unsigned __int8 *)(v7 + 185));
      if ( result != 0 )
      {
        result = sub_140D83E70(result, v6, (unsigned int)&dword_141AAE084, 0, 0, 0);
        if ( result != 0 )
        {
          v8 = *(unsigned __int8 *)(result + 86);
          if ( v8 != 13 && v8 != 26 )
          {
            v9 = *(__int16 *)(result + 72);
            v10 = ((unsigned int)(5243 * v9) >> 31) + ((5243 * v9) >> 19);
            v11 = (__int16)v9 % 100;
            v12 = (unsigned __int16)dword_141AAE084 >> 9;
            if ( v12 != 0 )
            {
              if ( v12 == 127 )
              {
                LOBYTE(v13) = 17;
                v14 = 55;
              }
              else
              {
                v15 = v12 - 1;
                v13 = (unsigned int)(5243
                                   * ((unsigned __int16)(100 * (unsigned __int8)(v15 / 4) + (char)(15 * (v15 % 4)) + 600) >> 2)) >> 17;
                v16 = 100 * ((unsigned __int8)v15 >> 2) + (unsigned __int8)(15 * (v15 & 3)) + 600;
                v14 = v16 - 100 * ((5243 * (v16 >> 2)) >> 17);
              }
            }
            else
            {
              LOBYTE(v13) = 24;
              v14 = 0;
            }
            result = v14;
            if ( v11 >= v14 )
            {
              *a2 = v10 - v13;
            }
            else
            {
              *a2 = ~(_BYTE)v13 + v10;
              LOBYTE(v11) = v11 + 60;
            }
            *a3 = v11 - v14;
            if ( *a2 < 0 )
            {
              *a2 = 0;
              *a3 = 0;
            }
          }
        }
      }
    }
  }
  return result;
}
