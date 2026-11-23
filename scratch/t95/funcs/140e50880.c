__int64 __fastcall sub_140E50880(__int64 a1, __int64 **a2, char a3)
{
  __int64 *v6; // rbp
  __int64 *v7; // rbx
  char *v8; // rbp
  char v10; // al
  unsigned int v11; // ecx
  int v12; // edx
  int v13; // edx
  __int64 *v14; // rbx
  __int64 *v15; // rbx
  __int64 v16; // rdx
  __int64 v17; // rax
  __int64 v18; // r8
  __int64 *v19; // rbx
  __int64 *v20; // rbx
  __int64 *v21; // rdi
  __int64 v22; // rdx
  __int64 v23; // rax
  int v24; // eax
  __int64 v25; // rcx
  __int64 *v26; // r14
  __int64 v27; // rax
  _QWORD *v28; // rdx
  __int64 v29; // r8
  __int64 *v30; // rbx
  __int64 *v31; // rbx
  __int64 *v32; // rbx
  __int64 *v33; // rbx
  __int64 *v34; // rbx
  __int64 *v35; // rbx
  __int64 *v36; // rbx
  __int64 *v37; // rbx
  __int64 *v38; // rbx
  __int64 *v39; // rbx
  __int64 *v40; // rbx
  __int64 *v41; // rbx
  __int64 *v42; // rbx
  char v43; // [rsp+2Bh] [rbp-3Dh] BYREF
  int v44; // [rsp+2Ch] [rbp-3Ch] BYREF
  __int64 v45; // [rsp+30h] [rbp-38h] BYREF

  v6 = *a2;
  v43 = 17;
  (*(void (__fastcall **)(__int64 *, char *, __int64))(*v6 + 40))(v6, &v43, 1);
  if ( *((_DWORD *)v6 + 4) != 0 )
    goto LABEL_3;
  v7 = *a2;
  v8 = (char *)(a1 + 101);
  (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 101, 1);
  if ( *((_DWORD *)v7 + 4) != 0 )
    goto LABEL_3;
  v10 = *v8;
  v11 = *v8;
  if ( v11 <= 0x13 && (v12 = 589856, _bittest(&v12, v10)) )
  {
    if ( (unsigned int)v10 > 0x13 )
      goto LABEL_30;
  }
  else
  {
    v23 = *(_QWORD *)(a1 + 48);
    if ( v23 != 0 )
    {
      v24 = *(_DWORD *)(v23 + 8);
      v25 = v24;
    }
    else
    {
      v24 = -1;
      v25 = -1;
    }
    v45 = v25;
    v26 = *a2;
    if ( BYTE5(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
    {
      v44 = v24;
      v27 = *v26;
      v28 = &v44;
      v29 = 4;
    }
    else
    {
      v27 = *v26;
      v28 = &v45;
      v29 = 8;
    }
    (*(void (__fastcall **)(__int64 *, _QWORD *, __int64))(v27 + 40))(v26, v28, v29);
    if ( *((_DWORD *)v26 + 4) != 0 )
      goto LABEL_3;
    v10 = *v8;
    v11 = *v8;
    if ( v11 > 0x13 )
      goto LABEL_30;
  }
  v13 = 852336;
  if ( _bittest(&v13, v11) )
  {
    if ( v10 != 4 )
    {
      LOBYTE(v8) = 1;
LABEL_15:
      if ( a3 == 0 )
        return (unsigned int)v8;
      v19 = *a2;
      (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 24, 8);
      if ( *((_DWORD *)v19 + 4) == 0 )
      {
        v20 = *a2;
        (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 8, 4);
        if ( *((_DWORD *)v20 + 4) == 0 )
        {
          v8 = (char *)*a2;
          (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 12, 4);
          if ( *((_DWORD *)v8 + 4) == 0 )
          {
            v21 = *a2;
            v22 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
            (*(void (__fastcall **)(__int64 *, __int64, __int64))(*v21 + 40))(v21, v22, 4);
            if ( *((_DWORD *)v21 + 4) == 0 )
            {
              LOBYTE(v8) = 1;
              return (unsigned int)v8;
            }
          }
        }
      }
      goto LABEL_3;
    }
    v14 = *a2;
    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 82, 2);
    if ( *((_DWORD *)v14 + 4) == 0 )
    {
      v15 = *a2;
      v16 = a1 + 90;
      v17 = **a2;
      v18 = 2;
      goto LABEL_12;
    }
    goto LABEL_3;
  }
LABEL_30:
  LODWORD(v8) = 0;
  if ( (unsigned __int8)sub_140F805C0(a2, *(_QWORD *)(a1 + 32), 0) != 0 )
  {
    LODWORD(v8) = 0;
    if ( (unsigned __int8)sub_140F805C0(a2, *(_QWORD *)(a1 + 40), 0) != 0 )
    {
      LODWORD(v8) = 0;
      if ( (unsigned __int8)sub_140F805C0(a2, *(_QWORD *)(a1 + 56), 0) != 0 )
      {
        v30 = *a2;
        (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 72, 4);
        if ( *((_DWORD *)v30 + 4) == 0 )
        {
          v31 = *a2;
          (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 76, 4);
          if ( *((_DWORD *)v31 + 4) == 0 )
          {
            v32 = *a2;
            (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 80, 2);
            if ( *((_DWORD *)v32 + 4) == 0 )
            {
              v33 = *a2;
              (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 82, 2);
              if ( *((_DWORD *)v33 + 4) == 0 )
              {
                v34 = *a2;
                (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 84, 2);
                if ( *((_DWORD *)v34 + 4) == 0 )
                {
                  v35 = *a2;
                  (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 86, 2);
                  if ( *((_DWORD *)v35 + 4) == 0 )
                  {
                    v36 = *a2;
                    (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 88, 2);
                    if ( *((_DWORD *)v36 + 4) == 0 )
                    {
                      v37 = *a2;
                      (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 90, 2);
                      if ( *((_DWORD *)v37 + 4) == 0 )
                      {
                        v38 = *a2;
                        (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 94, 2);
                        if ( *((_DWORD *)v38 + 4) == 0 )
                        {
                          v39 = *a2;
                          (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 96, 2);
                          if ( *((_DWORD *)v39 + 4) == 0 )
                          {
                            v40 = *a2;
                            (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 98, 2);
                            if ( *((_DWORD *)v40 + 4) == 0 )
                            {
                              v41 = *a2;
                              (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 100, 1);
                              if ( *((_DWORD *)v41 + 4) == 0 )
                              {
                                v42 = *a2;
                                (*(void (__fastcall **)(__int64 *, __int64, __int64))(**a2 + 40))(*a2, a1 + 102, 1);
                                if ( *((_DWORD *)v42 + 4) == 0 )
                                {
                                  v15 = *a2;
                                  v16 = a1 + 104;
                                  v17 = **a2;
                                  v18 = 1;
LABEL_12:
                                  (*(void (__fastcall **)(__int64 *, __int64, __int64))(v17 + 40))(v15, v16, v18);
                                  LOBYTE(v8) = *((_DWORD *)v15 + 4) == 0;
                                  if ( *((_DWORD *)v15 + 4) != 0 )
                                    return (unsigned int)v8;
                                  goto LABEL_15;
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
LABEL_3:
        LODWORD(v8) = 0;
      }
    }
  }
  return (unsigned int)v8;
}
