__int64 __fastcall sub_141456A50(__int64 a1, int a2, __int64 **a3)
{
  unsigned int v5; // edi
  int v6; // r14d
  __int64 v7; // rax
  __int64 v8; // r8
  __int64 v9; // rdx
  unsigned __int64 v10; // rdx
  __int64 v11; // rbx
  __int64 v12; // rax
  int v13; // ecx
  char v14; // bl
  __int64 v15; // rax
  __int64 *v16; // rax
  __int64 *v17; // rcx
  int v18; // eax
  signed int v19; // ecx
  __int64 *v20; // rax
  __int64 *v21; // rcx
  char v22; // bl
  __int64 *v23; // rax
  __int64 *v24; // rcx
  __int64 *v25; // rax
  __int64 *v26; // rcx
  __int64 *v27; // rax
  __int64 *v28; // rcx
  __int64 v29; // rdx
  __int64 *v30; // rcx
  __int64 *v31; // rax
  __int64 *v32; // rcx
  __int64 v33; // r8
  __int64 v34; // rdx
  unsigned __int64 v35; // rdx
  __int64 v36; // rbx
  signed int v37; // ecx
  __int64 *v39; // [rsp+28h] [rbp-18h] BYREF
  __int64 *v40; // [rsp+30h] [rbp-10h]
  __int64 v41; // [rsp+38h] [rbp-8h]

  v41 = -2;
  v5 = 0;
  if ( a2 > 1886151010 )
  {
    if ( a2 <= 1952801132 )
    {
      if ( a2 == 1886151011 )
      {
        v5 = *(char *)(a1 + 44);
        v15 = sub_14083D4F0(a1) + 40;
        LODWORD(v40) = v5;
        v39 = (__int64 *)v15;
        if ( &v39 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v27 = v39;
          v28 = v40;
          a3[1] = v40;
          *a3 = v27;
          v15 = sub_14083D4F0(v28) + 8;
          v40 = nullptr;
          v39 = (__int64 *)v15;
        }
      }
      else
      {
        if ( a2 != 1886547821 )
          return v5;
        v14 = *(_BYTE *)(a1 + 46) & 1;
        v15 = sub_14083D4F0(a1) + 24;
        LOBYTE(v40) = v14;
        v39 = (__int64 *)v15;
        if ( &v39 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v16 = v39;
          v17 = v40;
          a3[1] = v40;
          *a3 = v16;
          v15 = sub_14083D4F0(v17) + 8;
          v40 = nullptr;
          v39 = (__int64 *)v15;
        }
      }
      goto LABEL_52;
    }
    if ( a2 != 2036687218 )
    {
      if ( a2 != 2003267699 )
      {
        if ( a2 == 1952801133 )
        {
          v5 = *(_DWORD *)(a1 + 28);
          v6 = -1;
          if ( v5 != -1 )
          {
            v7 = sub_140F74650(qword_141B5FE40, v5);
            if ( v7 == 0 )
            {
              if ( (v5 & 0x80000000) == 0 && (_BYTE)word_141B60320 == 0 )
              {
                v8 = *(_QWORD *)(qword_141B5FE40 + 96);
                v9 = *(_QWORD *)(qword_141B5FE40 + 104) - v8;
                if ( v9 != 0 )
                {
                  v10 = v9 >> 3;
                  v11 = 0;
                  while ( 1 )
                  {
                    v7 = *(_QWORD *)(v8 + 8 * v11);
                    if ( v7 != 0 )
                    {
                      v19 = *(_DWORD *)(v7 + 12);
                      if ( v19 == v5 )
                        goto LABEL_30;
                      if ( v19 > (int)v5 )
                        break;
                    }
                    if ( ++v11 >= v10 )
                      goto LABEL_72;
                  }
                }
              }
              goto LABEL_72;
            }
LABEL_29:
            v5 = *(_DWORD *)(v7 + 12);
LABEL_30:
            v18 = *(_DWORD *)(v7 + 16);
            if ( v18 == 0 )
              v18 = v5;
            v6 = v5;
            goto LABEL_73;
          }
          goto LABEL_72;
        }
        return v5;
      }
      v22 = *(_BYTE *)(a1 + 46);
      v15 = sub_14083D4F0(a1) + 24;
      LOBYTE(v40) = (v22 & 4) != 0;
      v39 = (__int64 *)v15;
      if ( &v39 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v23 = v39;
        v24 = v40;
        a3[1] = v40;
        *a3 = v23;
        v15 = sub_14083D4F0(v24) + 8;
        v40 = nullptr;
        v39 = (__int64 *)v15;
      }
LABEL_52:
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v15 + 16LL))(v15, &v39);
LABEL_75:
      LOBYTE(v5) = 1;
      return v5;
    }
    if ( (*(_WORD *)(a1 + 36) & 0x1FF) == 0 )
    {
      v5 = *(unsigned __int16 *)(a1 + 38);
      if ( v5 != 1900 )
      {
        v15 = sub_14083D4F0(a1) + 40;
        LODWORD(v40) = v5;
        v39 = (__int64 *)v15;
        if ( &v39 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v20 = v39;
          v21 = v40;
          a3[1] = v40;
          *a3 = v20;
          v15 = sub_14083D4F0(v21) + 8;
          v40 = nullptr;
          v39 = (__int64 *)v15;
        }
        goto LABEL_52;
      }
    }
LABEL_56:
    LOBYTE(v5) = 1;
    if ( a3 != (__int64 **)&qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return v5;
  }
  if ( a2 <= 1684108388 )
  {
    if ( a2 != 1634365282 )
    {
      if ( a2 == 1668246896 )
      {
        v5 = -1;
        if ( *(_DWORD *)(a1 + 32) == -1 )
        {
          v13 = -1;
        }
        else
        {
          v12 = sub_140F45DB0(qword_141B5FDC0);
          v13 = -1;
          if ( v12 != 0 )
          {
            v5 = *(_DWORD *)(v12 + 12);
            v13 = *(_DWORD *)(v12 + 16);
            if ( v13 == 0 )
              v13 = *(_DWORD *)(v12 + 12);
          }
        }
        v39 = (__int64 *)__PAIR64__(v13, v5);
        v29 = 1668246896;
        goto LABEL_74;
      }
      return v5;
    }
    v5 = *(unsigned __int8 *)(a1 + 45);
    if ( *(_BYTE *)(a1 + 45) != 0 )
    {
      v15 = sub_14083D4F0(a1) + 56;
      LODWORD(v40) = v5;
      v39 = (__int64 *)v15;
      if ( &v39 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v25 = v39;
        v26 = v40;
        a3[1] = v40;
        *a3 = v25;
        v15 = sub_14083D4F0(v26) + 8;
        v40 = nullptr;
        v39 = (__int64 *)v15;
      }
      goto LABEL_52;
    }
    goto LABEL_56;
  }
  if ( a2 == 1684108389 )
  {
    if ( (*(_WORD *)(a1 + 36) & 0x1FF) != 0 && (*(_WORD *)(a1 + 38) != 1900 || (*(_WORD *)(a1 + 36) & 0x1FF) != 1) )
    {
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
      LODWORD(v40) = ((*(_WORD *)(a1 + 36) & 0x1FF) << 8)
                   | (*(unsigned __int16 *)(a1 + 36) >> 9)
                   | (*(unsigned __int16 *)(a1 + 38) << 17);
      v30 = &qword_141B5C8A0;
      v39 = &qword_141B5C8A0;
      if ( &v39 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v31 = v39;
        v32 = v40;
        a3[1] = v40;
        *a3 = v31;
        v30 = (__int64 *)(sub_14083D4F0(v32) + 8);
        v40 = nullptr;
        v39 = v30;
      }
      (*(void (__fastcall **)(__int64 *, __int64 **))(*v30 + 16))(v30, &v39);
      goto LABEL_75;
    }
    goto LABEL_56;
  }
  if ( a2 == 1869899105 )
  {
    v5 = *(_DWORD *)(a1 + 40);
    v6 = -1;
    if ( v5 != -1 )
    {
      v7 = sub_140F74650(qword_141B5FE40, v5);
      if ( v7 == 0 )
      {
        if ( (v5 & 0x80000000) == 0 && (_BYTE)word_141B60320 == 0 )
        {
          v33 = *(_QWORD *)(qword_141B5FE40 + 96);
          v34 = *(_QWORD *)(qword_141B5FE40 + 104) - v33;
          if ( v34 != 0 )
          {
            v35 = v34 >> 3;
            v36 = 0;
            while ( 1 )
            {
              v7 = *(_QWORD *)(v33 + 8 * v36);
              if ( v7 != 0 )
              {
                v37 = *(_DWORD *)(v7 + 12);
                if ( v37 == v5 )
                  goto LABEL_30;
                if ( v37 > (int)v5 )
                  break;
              }
              if ( ++v36 >= v35 )
                goto LABEL_72;
            }
          }
        }
        goto LABEL_72;
      }
      goto LABEL_29;
    }
LABEL_72:
    v18 = -1;
LABEL_73:
    v39 = (__int64 *)__PAIR64__(v18, v6);
    v29 = 1416914273;
LABEL_74:
    sub_140FE72B0(&v39, v29, a3);
    goto LABEL_75;
  }
  return v5;
}
