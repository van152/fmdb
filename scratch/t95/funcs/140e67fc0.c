char __fastcall sub_140E67FC0(_QWORD *a1, char a2)
{
  __int64 v2; // rax
  __int64 v5; // rdi
  __int64 v6; // rcx
  __int64 v7; // rdi
  _QWORD *v8; // r15
  _QWORD *v9; // rdi
  _QWORD *v10; // r14
  _QWORD *v11; // rdi
  _QWORD *v12; // rbx
  __int64 v13; // rbx
  int v14; // r8d
  unsigned __int64 v15; // rdx
  bool v16; // cl
  __int64 v17; // rbx
  __int64 v18; // rcx
  __int64 *v19; // rbp
  __int64 *i; // rbx
  __int64 v21; // rdi
  _QWORD *v22; // r12
  __int64 *v23; // rax
  __int64 v24; // rax
  __int64 v25; // r14
  __int64 v26; // rcx
  __int64 *v27; // r13
  __int64 v28; // r9
  unsigned __int64 v29; // r9
  __int64 j; // r14
  __int64 v31; // rdx
  char v32; // cl
  unsigned __int64 v33; // r15
  __int64 v34; // rcx

  v2 = a1[3];
  if ( v2 != a1[4] )
  {
    v2 = *(_QWORD *)v2;
    if ( v2 != 0 )
    {
      v5 = *(_QWORD *)(v2 + 48);
      if ( v5 != 0 )
        v5 = *(_QWORD *)(v2 + 80);
      if ( v5 != 0 && a1[27] != 0 )
      {
        v6 = *(_QWORD *)(v5 + 176);
        if ( v6 != 0 )
        {
          LOBYTE(v2) = sub_1409083C0(v6);
          if ( (_BYTE)v2 != 0 )
          {
            v7 = *(_QWORD *)(v5 + 176);
            if ( v7 == 0
              || (LOBYTE(v2) = sub_1409083C0(v7), (_BYTE)v2 == 0)
              || *(_BYTE *)(v7 + 840) != 1
              && (*(_BYTE *)(v7 + 53) & 0x20) == 0
              && ((v2 = *(_QWORD *)(v7 + 520)) == 0 || *(_BYTE *)(v2 + 522) != 1) )
            {
              v8 = *(_QWORD **)(a1[32] + 48LL);
              if ( v8 != nullptr )
                goto LABEL_19;
              v9 = (_QWORD *)sub_140DD0C30(24);
              if ( qword_141ABD470 == 0 )
                qword_141ABD470 = sub_1407E4940();
              v9[2] = 0;
              v9[1] = 0;
              *v9 = 0;
              *(_QWORD *)(a1[32] + 48LL) = v9;
              v2 = a1[32];
              v8 = *(_QWORD **)(v2 + 48);
              if ( v8 != nullptr )
              {
LABEL_19:
                v10 = (_QWORD *)*v8;
                v11 = (_QWORD *)v8[1];
                if ( (_QWORD *)*v8 != v11 )
                {
                  v12 = (_QWORD *)*v8;
                  do
                  {
                    if ( *v12 != 0 )
                      sub_140DD5820();
                    ++v12;
                  }
                  while ( v12 != v11 );
                  v13 = v8[1] - (_QWORD)v11;
                  sub_141758A00();
                  v8[1] = (char *)v10 + v13;
                  v8 = *(_QWORD **)(a1[32] + 48LL);
                }
                sub_140E68400(a1, v8, 0);
                sub_140E68730(a1, *(_QWORD *)(a1[32] + 48LL));
                v2 = a1[27];
                v15 = (unsigned int)(*(_DWORD *)(v2 + 12) - 763);
                if ( (unsigned int)v15 >= 0x28 || (v16 = true, v17 = 0x8300002101LL, !_bittest64(&v17, v15)) )
                {
                  v2 = *(_QWORD *)(v2 + 248);
                  if ( v2 == 0 )
                    goto LABEL_35;
                  v16 = *(_DWORD *)(v2 + 12) == 14;
                }
                if ( v16 && a2 != 0 )
                {
                  v2 = a1[3];
                  if ( v2 == a1[4] )
                    return v2;
                  v18 = *(_QWORD *)v2;
                  if ( *(_QWORD *)v2 == 0 )
                    return v2;
                  v2 = *(_BYTE *)(v18 + 40) != 0 ? sub_1411A41D0() : *(_QWORD *)(v18 + 128);
                  if ( v2 == 0 )
                    return v2;
                  v34 = v2 + *(int *)(*(_QWORD *)(v2 + 8) + 4LL) + 8;
                  v2 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v34 + 1760LL))(v34);
                  if ( v2 == 0 )
                    return v2;
                  goto LABEL_36;
                }
LABEL_35:
                if ( a2 == 0 )
                  return v2;
LABEL_36:
                v19 = (__int64 *)a1[35];
                for ( i = (__int64 *)a1[36]; v19 != i; ++v19 )
                {
                  v21 = *v19;
                  LODWORD(v2) = *(unsigned __int8 *)(*v19 + 48);
                  if ( (_DWORD)v2 != 17 && (_DWORD)v2 != 24 && (*(_BYTE *)(v21 + 21) & 0x20) == 0 )
                  {
                    LODWORD(v2) = *(_DWORD *)(v21 + 28);
                    if ( (v2 & 0x40000000) == 0 && (*(_QWORD **)v21 == a1 || (v2 & 0x4000) != 0) )
                    {
                      v22 = *(_QWORD **)(v21 + 8);
                      if ( v22 != nullptr )
                      {
                        if ( v22 != a1 || (v2 & 0x4000) == 0 || (v22 = *(_QWORD **)v21, *(_QWORD *)v21 != 0) )
                        {
                          if ( (v2 & 8) != 0 )
                          {
                            LOBYTE(v14) = 100;
                            LOBYTE(v2) = sub_1413FB4C0(*(_QWORD *)(a1[32] + 48LL), v22[27], v14, 0, (__int64)v22, 0);
                          }
                          else
                          {
                            v23 = (__int64 *)v22[3];
                            if ( v23 == (__int64 *)v22[4] )
                              goto LABEL_60;
                            v24 = *v23;
                            if ( v24 == 0 )
                              goto LABEL_60;
                            v25 = *(_QWORD *)(v24 + 48);
                            if ( v25 != 0 )
                              v25 = *(_QWORD *)(v24 + 80);
                            if ( v25 != 0
                              && v22[27] != 0
                              && (v26 = *(_QWORD *)(v25 + 176)) != 0
                              && sub_1409083C0(v26)
                              && (unsigned __int8)sub_140ECF770(v25) == 0 )
                            {
                              sub_140E67FC0(v22, 0);
                              v2 = v22[32];
                              v27 = *(__int64 **)(v2 + 48);
                              if ( v27 != nullptr )
                              {
                                v28 = v27[1] - *v27;
                                if ( v28 != 0 )
                                {
                                  v29 = v28 >> 3;
                                  if ( v29 < 2 )
                                    v29 = 1;
                                  for ( j = 0; j != v29; ++j )
                                  {
                                    v2 = *v27;
                                    v31 = *(_QWORD *)(*v27 + 8 * j);
                                    if ( v31 != 0 )
                                    {
                                      v32 = 2 * ((*(_BYTE *)(v21 + 29) & 0x40) == 0) + 3;
                                      LODWORD(v2) = *(char *)(v31 + 36);
                                      LOBYTE(v2) = *(char *)(v31 + 36) / v32;
                                      if ( (char)v2 >= 20 )
                                      {
                                        v33 = v29;
                                        BYTE1(v2) = *(char *)(v31 + 36) % v32;
                                        LOBYTE(v2) = sub_1413FB4C0(
                                                       *(_QWORD *)(a1[32] + 48LL),
                                                       *(_QWORD *)v31,
                                                       v2,
                                                       0,
                                                       (__int64)v22,
                                                       0);
                                        v29 = v33;
                                      }
                                    }
                                  }
                                }
                              }
                            }
                            else
                            {
LABEL_60:
                              sub_140E68400(v22, *(_QWORD *)(a1[32] + 48LL), v22);
                              LOBYTE(v2) = sub_140E68730(v22, *(_QWORD *)(a1[32] + 48LL));
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return v2;
}
