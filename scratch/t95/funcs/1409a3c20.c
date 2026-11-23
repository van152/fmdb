// THUNK ALIAS -> sub_1438D4C20 (jmp:0x1409a3c20->0x1438d4c20)
float __fastcall sub_1438D4C20(__int64 a1)
{
  _QWORD *v2; // rdi
  _QWORD *v3; // rbx
  float result; // xmm0_4
  __int64 v5; // r8
  __int64 v6; // r9
  __int64 v7; // rax
  float v8; // xmm0_4
  __int64 *v9; // rax
  __int64 v10; // r9
  __int64 v11; // rax
  unsigned __int64 v12; // rax
  __int64 v13; // r10
  __int64 v14; // rdx
  __int64 v15; // r8
  __int64 v16; // rbx
  int v17; // eax
  unsigned __int64 v18; // rcx
  int v19; // eax

  v2 = *(_QWORD **)(a1 + 496);
  v3 = *(_QWORD **)(a1 + 504);
  if ( v2 == v3 )
  {
LABEL_4:
    result = *(float *)(a1 + 1616);
    if ( result == 0.0 )
    {
      MEMORY[0x141947418](a1 + 8);
      if ( *(float *)(a1 + 1616) == 0.0 )
      {
        LOBYTE(v5) = -1;
        LOBYTE(v6) = -1;
        v7 = sub_140926260(a1, 0, v5, v6);
        v8 = MEMORY[0x141759000];
        if ( v7 != 0 )
        {
          v9 = *(__int64 **)(v7 + 88);
          if ( v9 != nullptr )
          {
            v10 = *v9;
            v11 = v9[1] - *v9;
            if ( v11 != 0 )
            {
              v12 = v11 >> 3;
              v13 = 1;
              if ( v12 >= 2 )
                v13 = v12;
              v14 = 0;
              v15 = 0x10000800001LL;
              while ( 1 )
              {
                v16 = *(_QWORD *)(v10 + 8 * v14);
                v17 = *(__int16 *)(v16 + 28);
                v18 = (unsigned int)(v17 - 70);
                if ( (unsigned int)v18 <= 0x28 )
                {
                  if ( _bittest64(&v15, v18) )
                    break;
                }
                if ( *(_WORD *)(v16 + 28) == 0 || v17 == 399 )
                  break;
                if ( v13 == ++v14 )
                  goto LABEL_20;
              }
              v19 = *(_DWORD *)(v16 + 24);
              if ( v19 >= 0 )
                v8 = (float)(v19 / 0x34u);
            }
          }
        }
LABEL_20:
        *(float *)(a1 + 1616) = v8;
      }
      MEMORY[0x141947608](a1 + 8);
      return *(float *)(a1 + 1616);
    }
  }
  else
  {
    while ( 1 )
    {
      result = (*(float (__fastcall **)(_QWORD, __int64))(*(_QWORD *)*v2 + 312LL))(*v2, a1);
      if ( result > 0.0 )
        break;
      if ( ++v2 == v3 )
        goto LABEL_4;
    }
  }
  return result;
}
