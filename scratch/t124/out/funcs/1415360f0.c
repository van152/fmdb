__int64 __fastcall sub_1415360F0(__int64 a1, int a2, __int64 **a3)
{
  __int64 **v5; // rdi
  __int64 v6; // rax
  __int64 *v7; // rax
  __int64 *v8; // rcx
  __int64 *v9; // rax
  __int64 *v10; // rcx
  __int64 *v11; // rax
  __int64 *v12; // rcx
  __int64 *v13; // rax
  __int64 *v14; // rcx
  __int64 *v15; // rax
  __int64 *v16; // rcx
  __int64 *v17; // rcx
  __int64 *v18; // rax
  __int64 *v19; // rcx
  __int64 *v20; // rax
  __int64 *v21; // rcx
  __int64 *v22; // rax
  __int64 *v23; // rcx
  __int64 *v24; // rax
  __int64 *v25; // rcx
  __int64 *v26; // rax
  __int64 *v27; // rcx
  __int64 *v28; // rax
  __int64 *v29; // rcx
  float v30; // xmm6_4
  __int64 *v31; // rax
  __int64 *v32; // rcx
  __int64 *v33; // rax
  __int64 *v34; // rcx
  __int64 v35; // rcx
  int v36; // eax
  int v37; // ecx
  __int64 *v38; // rax
  __int64 *v39; // rcx
  __int64 *v40; // rax
  __int64 *v41; // rcx
  __int64 *v43; // [rsp+28h] [rbp-28h] BYREF
  __int64 *v44; // [rsp+30h] [rbp-20h]
  __int64 v45; // [rsp+38h] [rbp-18h]

  v45 = -2;
  LODWORD(v5) = 0;
  if ( a2 > 1667330919 )
  {
    if ( a2 > 1768845939 )
    {
      if ( a2 <= 1937007731 )
      {
        if ( a2 != 1768845940 )
        {
          if ( a2 == 1936684402 )
          {
            LODWORD(v5) = *(char *)(a1 + 94);
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v44) = (_DWORD)v5;
            v43 = (__int64 *)v6;
            if ( &v43 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v13 = v43;
              v14 = v44;
              a3[1] = v44;
              *a3 = v13;
              v6 = sub_14083D4F0(v14) + 8;
              v44 = nullptr;
              v43 = (__int64 *)v6;
            }
            goto LABEL_74;
          }
          return (unsigned int)v5;
        }
        v30 = *(float *)(a1 + 64);
        if ( v30 == MEMORY[0x1418BD598] )
        {
          v6 = sub_14083D4F0(a1) + 104;
          LODWORD(v44) = 0;
          v43 = (__int64 *)v6;
          if ( &v43 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v31 = v43;
            v32 = v44;
            a3[1] = v44;
            *a3 = v31;
            v6 = sub_14083D4F0(v32) + 8;
            v44 = nullptr;
            v43 = (__int64 *)v6;
          }
          goto LABEL_74;
        }
        if ( v30 != MEMORY[0x141759000] )
        {
          LODWORD(v44) = *(_DWORD *)(a1 + 64);
          v43 = (__int64 *)(sub_14083D4F0(a1) + 104);
          v5 = &v43;
          sub_14083DFA0(a3, &v43);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v43 + 16))(v43, &v43);
          goto LABEL_84;
        }
        goto LABEL_80;
      }
      if ( a2 != 1937007732 )
      {
        if ( a2 == 2036687218 )
        {
          LODWORD(v5) = *(unsigned __int16 *)(a1 + 58);
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v44) = (_DWORD)v5;
          v43 = (__int64 *)v6;
          if ( &v43 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v22 = v43;
            v23 = v44;
            a3[1] = v44;
            *a3 = v22;
            v6 = sub_14083D4F0(v23) + 8;
            v44 = nullptr;
            v43 = (__int64 *)v6;
          }
          goto LABEL_74;
        }
        return (unsigned int)v5;
      }
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      LODWORD(v44) = ((*(_WORD *)(a1 + 56) & 0x1FF) << 8)
                   | (*(unsigned __int16 *)(a1 + 56) >> 9)
                   | (*(unsigned __int16 *)(a1 + 58) << 17);
      v17 = &qword_141B5C8A0;
      v43 = &qword_141B5C8A0;
      if ( &v43 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v40 = v43;
        v41 = v44;
        a3[1] = v44;
        *a3 = v40;
        v17 = (__int64 *)(sub_14083D4F0(v41) + 8);
        v44 = nullptr;
        v43 = v17;
      }
    }
    else
    {
      if ( a2 <= 1668246895 )
      {
        if ( a2 == 1667330920 )
        {
          LODWORD(v5) = *(_DWORD *)(a1 + 40);
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v44) = (_DWORD)v5;
          v43 = (__int64 *)v6;
          if ( &v43 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v26 = v43;
            v27 = v44;
            a3[1] = v44;
            *a3 = v26;
            v6 = sub_14083D4F0(v27) + 8;
            v44 = nullptr;
            v43 = (__int64 *)v6;
          }
          goto LABEL_74;
        }
        if ( a2 == 1668182625 )
        {
          LODWORD(v5) = *(_DWORD *)(a1 + 76);
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v44) = (_DWORD)v5;
          v43 = (__int64 *)v6;
          if ( &v43 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v9 = v43;
            v10 = v44;
            a3[1] = v44;
            *a3 = v9;
            v6 = sub_14083D4F0(v10) + 8;
            v44 = nullptr;
            v43 = (__int64 *)v6;
          }
          goto LABEL_74;
        }
        return (unsigned int)v5;
      }
      if ( a2 == 1668246896 )
      {
        v35 = *(_QWORD *)(a1 + 32);
        if ( v35 != 0 )
        {
          v36 = *(_DWORD *)(v35 + 12);
          v37 = *(_DWORD *)(v35 + 16);
          if ( v37 == 0 )
            v37 = v36;
        }
        else
        {
          v36 = -1;
          v37 = -1;
        }
        v43 = (__int64 *)__PAIR64__(v37, v36);
        sub_140FE72B0(&v43, 1668246896, a3);
        goto LABEL_84;
      }
      if ( a2 != 1701733492 )
        return (unsigned int)v5;
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      LODWORD(v44) = ((*(_WORD *)(a1 + 60) & 0x1FF) << 8)
                   | (*(unsigned __int16 *)(a1 + 60) >> 9)
                   | (*(unsigned __int16 *)(a1 + 62) << 17);
      v17 = &qword_141B5C8A0;
      v43 = &qword_141B5C8A0;
      if ( &v43 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v18 = v43;
        v19 = v44;
        a3[1] = v44;
        *a3 = v18;
        v17 = (__int64 *)(sub_14083D4F0(v19) + 8);
        v44 = nullptr;
        v43 = v17;
      }
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v17 + 16))(v17, &v43);
LABEL_84:
    LOBYTE(v5) = 1;
    return (unsigned int)v5;
  }
  if ( a2 > 1131639407 )
  {
    if ( a2 <= 1131700852 )
    {
      if ( a2 == 1131639408 )
      {
        LODWORD(v5) = *(char *)(a1 + 95);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v44) = (_DWORD)v5;
        v43 = (__int64 *)v6;
        if ( &v43 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v28 = v43;
          v29 = v44;
          a3[1] = v44;
          *a3 = v28;
          v6 = sub_14083D4F0(v29) + 8;
          v44 = nullptr;
          v43 = (__int64 *)v6;
        }
        goto LABEL_74;
      }
      if ( a2 == 1131639417 )
      {
        LODWORD(v5) = *(_DWORD *)(a1 + 80);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v44) = (_DWORD)v5;
        v43 = (__int64 *)v6;
        if ( &v43 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v11 = v43;
          v12 = v44;
          a3[1] = v44;
          *a3 = v11;
          v6 = sub_14083D4F0(v12) + 8;
          v44 = nullptr;
          v43 = (__int64 *)v6;
        }
        goto LABEL_74;
      }
      return (unsigned int)v5;
    }
    if ( a2 != 1131700853 )
    {
      if ( a2 == 1131704940 )
      {
        LODWORD(v5) = *(_DWORD *)(a1 + 84);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v44) = (_DWORD)v5;
        v43 = (__int64 *)v6;
        if ( &v43 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v20 = v43;
          v21 = v44;
          a3[1] = v44;
          *a3 = v20;
          v6 = sub_14083D4F0(v21) + 8;
          v44 = nullptr;
          v43 = (__int64 *)v6;
        }
        goto LABEL_74;
      }
      return (unsigned int)v5;
    }
    LODWORD(v5) = *(_DWORD *)(a1 + 44);
    if ( (_DWORD)v5 != -1 )
    {
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v44) = (_DWORD)v5;
      v43 = (__int64 *)v6;
      if ( &v43 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v38 = v43;
        v39 = v44;
        a3[1] = v44;
        *a3 = v38;
        v6 = sub_14083D4F0(v39) + 8;
        v44 = nullptr;
        v43 = (__int64 *)v6;
      }
      goto LABEL_74;
    }
    goto LABEL_80;
  }
  if ( a2 > 1131441259 )
  {
    if ( a2 == 1131441260 )
    {
      LODWORD(v5) = *(_DWORD *)(a1 + 88);
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v44) = (_DWORD)v5;
      v43 = (__int64 *)v6;
      if ( &v43 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v33 = v43;
        v34 = v44;
        a3[1] = v44;
        *a3 = v33;
        v6 = sub_14083D4F0(v34) + 8;
        v44 = nullptr;
        v43 = (__int64 *)v6;
      }
      goto LABEL_74;
    }
    if ( a2 != 1131572578 )
      return (unsigned int)v5;
    LODWORD(v5) = *(_DWORD *)(a1 + 48);
    if ( (_DWORD)v5 != 0 )
    {
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v44) = (_DWORD)v5;
      v43 = (__int64 *)v6;
      if ( &v43 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v15 = v43;
        v16 = v44;
        a3[1] = v44;
        *a3 = v15;
        v6 = sub_14083D4F0(v16) + 8;
        v44 = nullptr;
        v43 = (__int64 *)v6;
      }
      goto LABEL_74;
    }
LABEL_80:
    LOBYTE(v5) = 1;
    if ( a3 != (__int64 **)&qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return (unsigned int)v5;
  }
  if ( a2 == 1129142085 )
  {
    LODWORD(v5) = *(_DWORD *)(a1 + 68);
    if ( (_DWORD)v5 != -1 )
    {
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v44) = (_DWORD)v5;
      v43 = (__int64 *)v6;
      if ( &v43 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v24 = v43;
        v25 = v44;
        a3[1] = v44;
        *a3 = v24;
        v6 = sub_14083D4F0(v25) + 8;
        v44 = nullptr;
        v43 = (__int64 *)v6;
      }
      goto LABEL_74;
    }
    goto LABEL_80;
  }
  if ( a2 == 1130587745 )
  {
    LODWORD(v5) = *(char *)(a1 + 96);
    v6 = sub_14083D4F0(a1) + 40;
    LODWORD(v44) = (_DWORD)v5;
    v43 = (__int64 *)v6;
    if ( &v43 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v7 = v43;
      v8 = v44;
      a3[1] = v44;
      *a3 = v7;
      v6 = sub_14083D4F0(v8) + 8;
      v44 = nullptr;
      v43 = (__int64 *)v6;
    }
LABEL_74:
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v43);
    goto LABEL_84;
  }
  return (unsigned int)v5;
}
