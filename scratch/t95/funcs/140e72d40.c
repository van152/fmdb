__int64 __fastcall sub_140E72D40(__int64 a1, char a2, char a3, char a4, unsigned __int8 a5)
{
  __int64 v6; // rax
  __int64 v7; // rcx
  unsigned __int64 v10; // rdx
  unsigned __int64 v11; // r13
  __int64 v12; // r14
  __int64 v13; // rbx
  __int64 v14; // r15
  char v15; // al
  _QWORD *v16; // rbp
  __int64 v17; // rcx
  __int64 v18; // rax
  _QWORD *v19; // rdi
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rax
  unsigned __int64 v24; // r13
  __int64 v25; // rbp
  __int64 v26; // rbx
  __int64 v27; // rsi
  char v28; // al
  __int64 v29; // rcx
  _QWORD *v30; // rdi
  __int64 v31; // rcx
  unsigned __int64 v32; // r15
  __int64 v33; // r13
  __int64 *v34; // rsi
  __int64 *v35; // rbx
  char v36; // al
  __int64 v37; // rbp
  __int64 v38; // rcx
  __int64 v39; // rax
  _QWORD *v40; // rdi
  __int64 v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rax
  unsigned __int64 v44; // r15
  __int64 v45; // r14
  __int64 v46; // rbx
  __int64 v47; // rsi
  char v48; // al
  _QWORD *v49; // rbp
  __int64 v50; // rcx
  __int64 v51; // rax
  _QWORD *v52; // rdi
  __int64 v53; // rcx
  __int64 v54; // rax
  __int64 v55; // rax
  __int64 v56; // [rsp+30h] [rbp-48h]

  v6 = *(_QWORD *)(a1 + 24);
  v7 = *(_QWORD *)(a1 + 32);
  if ( v7 == v6 )
    return 0;
  v10 = 0;
  if ( a4 != 0 )
  {
    if ( a2 != 0 )
    {
      if ( a3 != 0 )
      {
        v56 = 0;
        v11 = 0;
        do
        {
          v12 = *(_QWORD *)(v6 + 8 * v11);
          if ( v12 != 0 )
          {
            v13 = *(_QWORD *)(v12 + 56);
            v14 = *(_QWORD *)(v12 + 64);
            if ( v13 != v14 )
            {
              do
              {
                v16 = *(_QWORD **)v13;
                if ( (*(unsigned __int8 (__fastcall **)(__int64, unsigned __int64))(*(_QWORD *)(*(_QWORD *)v13
                                                                                              + *(int *)(*(_QWORD *)(*(_QWORD *)v13 + 8LL) + 4LL)
                                                                                              + 8LL)
                                                                                  + 1312LL))(
                       v7,
                       v10) == 0
                  && (unsigned __int8)sub_1410D43A0(v16, a1) == 0
                  && ((*(__int64 (__fastcall **)(_QWORD *))(*v16 + 1048LL))(v16) == 0
                   || (*(_BYTE *)((*(__int64 (__fastcall **)(_QWORD *))(*v16 + 1048LL))(v16) + 47) & 1) == 0)
                  && (unsigned __int8)sub_1410D6360(v16, a1) == 0 )
                {
                  v17 = (__int64)v16 + *(int *)(v16[1] + 4LL) + 8;
                  v18 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v17 + 1728LL))(v17);
                  if ( v18 != 0 )
                  {
                    v19 = (_QWORD *)v18;
                    v20 = v18 + *(int *)(*(_QWORD *)(v18 + 8) + 4LL) + 8;
                    v21 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v20 + 672LL))(v20);
                    if ( (unsigned __int8)sub_140E0A1C0(v19, v21) == 0 )
                    {
                      v22 = (*(__int64 (__fastcall **)(_QWORD *))(*v19 + 1048LL))(v19);
                      if ( v22 == 0
                        || (*(_BYTE *)(v22 + 46) & 8) == 0
                        || qword_141B5D668 == 0
                        || (char)sub_140B78B00(
                                   (int)v19 + *(_DWORD *)(v19[1] + 4LL) + 8,
                                   *(_QWORD *)(qword_141B5D668 + 96),
                                   0,
                                   0,
                                   124518401,
                                   0) >= 26 )
                      {
                        v15 = sub_141095D30((char *)v16 + *(int *)(v16[1] + 4LL) + 8, v12, a5);
                        v7 = v56;
                        LOBYTE(v7) = v15 + v56;
                        v56 = v7;
                      }
                    }
                  }
                }
                v13 += 8;
              }
              while ( v13 != v14 );
              v6 = *(_QWORD *)(a1 + 24);
              v7 = *(_QWORD *)(a1 + 32);
            }
          }
          ++v11;
          v10 = (v7 - v6) >> 3;
        }
        while ( v11 < v10 );
      }
      else
      {
        v56 = 0;
        v44 = 0;
        do
        {
          v45 = *(_QWORD *)(v6 + 8 * v44);
          if ( v45 != 0 )
          {
            v46 = *(_QWORD *)(v45 + 56);
            v47 = *(_QWORD *)(v45 + 64);
            if ( v46 != v47 )
            {
              do
              {
                v49 = *(_QWORD **)v46;
                if ( (*(unsigned __int8 (__fastcall **)(__int64, unsigned __int64))(*(_QWORD *)(*(_QWORD *)v46
                                                                                              + *(int *)(*(_QWORD *)(*(_QWORD *)v46 + 8LL) + 4LL)
                                                                                              + 8LL)
                                                                                  + 1312LL))(
                       v7,
                       v10) == 0
                  && (unsigned __int8)sub_1410D43A0(v49, a1) == 0
                  && ((*(__int64 (__fastcall **)(_QWORD *))(*v49 + 1048LL))(v49) == 0
                   || (*(_BYTE *)((*(__int64 (__fastcall **)(_QWORD *))(*v49 + 1048LL))(v49) + 47) & 1) == 0) )
                {
                  v50 = (__int64)v49 + *(int *)(v49[1] + 4LL) + 8;
                  v51 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v50 + 1728LL))(v50);
                  if ( v51 != 0 )
                  {
                    v52 = (_QWORD *)v51;
                    v53 = v51 + *(int *)(*(_QWORD *)(v51 + 8) + 4LL) + 8;
                    v54 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v53 + 672LL))(v53);
                    if ( (unsigned __int8)sub_140E0A1C0(v52, v54) == 0 )
                    {
                      v55 = (*(__int64 (__fastcall **)(_QWORD *))(*v52 + 1048LL))(v52);
                      if ( v55 == 0
                        || (*(_BYTE *)(v55 + 46) & 8) == 0
                        || qword_141B5D668 == 0
                        || (char)sub_140B78B00(
                                   (int)v52 + *(_DWORD *)(v52[1] + 4LL) + 8,
                                   *(_QWORD *)(qword_141B5D668 + 96),
                                   0,
                                   0,
                                   124518401,
                                   0) >= 26 )
                      {
                        v48 = sub_141095D30((char *)v49 + *(int *)(v49[1] + 4LL) + 8, v45, a5);
                        v7 = v56;
                        LOBYTE(v7) = v48 + v56;
                        v56 = v7;
                      }
                    }
                  }
                }
                v46 += 8;
              }
              while ( v46 != v47 );
              v6 = *(_QWORD *)(a1 + 24);
              v7 = *(_QWORD *)(a1 + 32);
            }
          }
          ++v44;
          v10 = (v7 - v6) >> 3;
        }
        while ( v44 < v10 );
      }
    }
    else
    {
      v56 = 0;
      v32 = 0;
      do
      {
        v33 = *(_QWORD *)(v6 + 8 * v32);
        if ( v33 != 0 )
        {
          v34 = *(__int64 **)(v33 + 56);
          v35 = *(__int64 **)(v33 + 64);
          if ( v34 != v35 )
          {
            do
            {
              v37 = *v34;
              if ( (*(unsigned __int8 (__fastcall **)(__int64, unsigned __int64))(*(_QWORD *)(*v34
                                                                                            + *(int *)(*(_QWORD *)(*v34 + 8) + 4LL)
                                                                                            + 8)
                                                                                + 1312LL))(
                     v7,
                     v10) == 0
                && (a3 == 0 || (unsigned __int8)sub_1410D6360(v37, a1) == 0) )
              {
                v38 = v37 + *(int *)(*(_QWORD *)(v37 + 8) + 4LL) + 8;
                v39 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v38 + 1728LL))(v38);
                if ( v39 != 0 )
                {
                  v40 = (_QWORD *)v39;
                  v41 = v39 + *(int *)(*(_QWORD *)(v39 + 8) + 4LL) + 8;
                  v42 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v41 + 672LL))(v41);
                  if ( (unsigned __int8)sub_140E0A1C0(v40, v42) == 0 )
                  {
                    v43 = (*(__int64 (__fastcall **)(_QWORD *))(*v40 + 1048LL))(v40);
                    if ( v43 == 0
                      || (*(_BYTE *)(v43 + 46) & 8) == 0
                      || qword_141B5D668 == 0
                      || (char)sub_140B78B00(
                                 (int)v40 + *(_DWORD *)(v40[1] + 4LL) + 8,
                                 *(_QWORD *)(qword_141B5D668 + 96),
                                 0,
                                 0,
                                 124518401,
                                 0) >= 26 )
                    {
                      v36 = sub_141095D30(v37 + *(int *)(*(_QWORD *)(v37 + 8) + 4LL) + 8, v33, a5);
                      v7 = v56;
                      LOBYTE(v7) = v36 + v56;
                      v56 = v7;
                    }
                  }
                }
              }
              ++v34;
            }
            while ( v34 != v35 );
            v6 = *(_QWORD *)(a1 + 24);
            v7 = *(_QWORD *)(a1 + 32);
          }
        }
        ++v32;
        v10 = (v7 - v6) >> 3;
      }
      while ( v32 < v10 );
    }
  }
  else
  {
    v56 = 0;
    v24 = 0;
    do
    {
      v25 = *(_QWORD *)(v6 + 8 * v24);
      if ( v25 != 0 )
      {
        v26 = *(_QWORD *)(v25 + 56);
        v27 = *(_QWORD *)(v25 + 64);
        if ( v26 != v27 )
        {
          do
          {
            v30 = *(_QWORD **)v26;
            v31 = *(_QWORD *)v26 + *(int *)(*(_QWORD *)(*(_QWORD *)v26 + 8LL) + 4LL) + 8LL;
            if ( (*(unsigned __int8 (__fastcall **)(__int64, unsigned __int64))(*(_QWORD *)v31 + 1312LL))(v31, v10) == 0
              && (a2 == 0
               || (unsigned __int8)sub_1410D43A0(v30, a1) == 0
               && ((*(__int64 (__fastcall **)(_QWORD *))(*v30 + 1048LL))(v30) == 0
                || (*(_BYTE *)((*(__int64 (__fastcall **)(_QWORD *))(*v30 + 1048LL))(v30) + 47) & 1) == 0))
              && (a3 == 0 || (unsigned __int8)sub_1410D6360(v30, a1) == 0) )
            {
              v28 = sub_141095D30((char *)v30 + *(int *)(v30[1] + 4LL) + 8, v25, a5);
              v29 = v56;
              LOBYTE(v29) = v28 + v56;
              v56 = v29;
            }
            v26 += 8;
          }
          while ( v26 != v27 );
          v6 = *(_QWORD *)(a1 + 24);
          v7 = *(_QWORD *)(a1 + 32);
        }
      }
      ++v24;
      v10 = (v7 - v6) >> 3;
    }
    while ( v24 < v10 );
  }
  return v56;
}
