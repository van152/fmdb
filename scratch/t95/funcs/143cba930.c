void __fastcall sub_143CBA930(__int64 a1, __int64 a2, __int64 *a3)
{
  __int64 *v3; // rsi
  __int64 i; // rbp
  __int64 v8; // rbx
  __int64 *v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 v12; // r15
  _QWORD *v13; // rbx
  __int64 v14; // r12
  unsigned __int64 v15; // rax
  unsigned __int64 v16; // r14
  unsigned __int64 v17; // rcx
  unsigned __int64 v18; // r14
  __int64 v19; // rdi
  _QWORD *v20; // r15
  __int64 v21; // r15
  __int64 v22; // rdi
  unsigned __int64 v23; // rcx
  __int64 v24; // rbx
  __int64 v25; // rbx
  bool v26; // al
  __int64 v27; // [rsp+20h] [rbp-58h]
  unsigned __int64 v28; // [rsp+28h] [rbp-50h]
  __int64 v29; // [rsp+30h] [rbp-48h]

  v3 = (__int64 *)qword_141B60060;
  for ( i = qword_141B60068; v3 != (__int64 *)i; ++v3 )
  {
    v8 = *v3;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v3 + 352LL))(*v3) == 0
      && (*(_BYTE *)(v8 + 353) & 1) == 0
      && sub_1408FF650(v8) == 0 )
    {
      v9 = *(__int64 **)(v8 + 24);
      if ( *(__int64 **)(v8 + 32) != v9 )
      {
        if ( a2 == 0 )
          goto LABEL_44;
        v10 = *(_QWORD *)(v8 + 216);
        if ( v10 != 0 )
        {
          if ( *(_BYTE *)(v8 + 185) == 0 || (v11 = *(_QWORD *)(v10 + 272)) == 0 )
            v11 = *(_QWORD *)(v10 + 264);
          if ( v11 == a2 )
          {
LABEL_44:
            if ( a1 == 0 || *(_QWORD *)(*(_QWORD *)(v8 + 216) + 240LL) == a1 || *(_DWORD *)(a1 + 12) == 7 )
            {
              v12 = *v9;
              if ( *v9 != 0 )
              {
                v13 = (_QWORD *)a3[1];
                if ( v13 == (_QWORD *)a3[2] )
                {
                  v27 = a2;
                  v29 = a1;
                  v14 = (__int64)v13 - *a3;
                  v15 = v14 >> 3;
                  v16 = (unsigned __int64)(v14 >> 3) >> 1;
                  v17 = 0x1FFFFFFFFFFFFFFFLL - v16;
                  v18 = (v14 >> 3) + v16;
                  v28 = (v14 >> 3) + 1;
                  if ( v18 <= v28 )
                    v18 = v15 + 1;
                  if ( v15 > v17 )
                    v18 = 0x1FFFFFFFFFFFFFFFLL;
                  v19 = sub_1407E4490(qword_141ABD470, 8 * v18);
                  *(_QWORD *)(v19 + v14) = v12;
                  v20 = (_QWORD *)a3[1];
                  sub_141758A00();
                  if ( v20 != v13 )
                    sub_141758A00();
                  v21 = v19;
                  v22 = *a3;
                  a2 = v27;
                  if ( *a3 != 0 )
                  {
                    v23 = a3[2] - v22;
                    if ( v23 == -1 )
                      v23 = *(unsigned int *)(v22 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v24 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v24) >> 3 > v23)
                      && (v25 = *(_QWORD *)(v24 + 8 * v23)) != 0 )
                    {
                      MEMORY[0x1419475D8](v25 + 32, v22 - *(unsigned int *)(v25 + 120));
                      v26 = *(_BYTE *)(v25 + 72) != 0
                         && _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) != 0;
                      if ( !v26 && *(_BYTE *)(v25 + 97) != 0 )
                        sub_1412D33C0(v25);
                    }
                    else
                    {
                      MEMORY[0x141948990](v22 - *(unsigned int *)(qword_141ABD470 + 48));
                    }
                  }
                  *a3 = v21;
                  a3[1] = v21 + 8 * v28;
                  a3[2] = v21 + 8 * v18;
                  a1 = v29;
                }
                else
                {
                  *v13 = v12;
                  a3[1] += 8;
                }
              }
            }
          }
        }
      }
    }
  }
}
