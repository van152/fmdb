__int64 __fastcall sub_141190B20(__int64 a1, int a2, __int64 **a3)
{
  unsigned int v5; // edi
  __int64 v6; // rax
  __int64 *v7; // rax
  __int64 *v8; // rcx
  __int64 *v9; // rcx
  __int64 *v10; // rax
  __int64 *v11; // rcx
  __int64 *v12; // rax
  __int64 *v13; // rcx
  __int64 *v14; // rax
  __int64 *v15; // rcx
  __int64 *v16; // rax
  __int64 *v17; // rcx
  __int64 *v18; // rax
  __int64 *v19; // rcx
  __int64 *v20; // rcx
  __int64 *v21; // rax
  __int64 *v22; // rcx
  __int64 *v24; // [rsp+20h] [rbp-10h] BYREF
  __int64 *v25; // [rsp+28h] [rbp-8h]
  __int64 v26; // [rsp+30h] [rbp+0h]

  v26 = -2;
  v5 = 0;
  if ( a2 <= 1835103330 )
  {
    if ( a2 == 1668052322 )
    {
      v5 = *(_DWORD *)(a1 + 48);
      if ( v5 != -1 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v25) = v5;
        v24 = (__int64 *)v6;
        if ( &v24 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v16 = v24;
          v17 = v25;
          a3[1] = v25;
          *a3 = v16;
          v6 = sub_14083D4F0(v17) + 8;
          v25 = nullptr;
          v24 = (__int64 *)v6;
        }
        goto LABEL_35;
      }
    }
    else
    {
      if ( a2 != 1668246896 )
      {
        if ( a2 == 1701733492 )
        {
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
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
          LODWORD(v25) = ((*(_WORD *)(a1 + 36) & 0x1FF) << 8)
                       | (*(unsigned __int16 *)(a1 + 36) >> 9)
                       | (*(unsigned __int16 *)(a1 + 38) << 17);
          v9 = &qword_141B5C8A0;
          v24 = &qword_141B5C8A0;
          if ( &v24 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v10 = v24;
            v11 = v25;
            a3[1] = v25;
            *a3 = v10;
            v9 = (__int64 *)(sub_14083D4F0(v11) + 8);
            v25 = nullptr;
            v24 = v9;
          }
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v9 + 16))(v9, &v24);
          LOBYTE(v5) = 1;
          if ( a3 != (__int64 **)&qword_141B5A4A0 && (*(_WORD *)(a1 + 36) & 0x1FF) == 1 && *(_WORD *)(a1 + 38) == 1900 )
            goto LABEL_37;
        }
        return v5;
      }
      v5 = *(_DWORD *)(a1 + 40);
      if ( v5 != -1 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v25) = v5;
        v24 = (__int64 *)v6;
        if ( &v24 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v18 = v24;
          v19 = v25;
          a3[1] = v25;
          *a3 = v18;
          v6 = sub_14083D4F0(v19) + 8;
          v25 = nullptr;
          v24 = (__int64 *)v6;
        }
        goto LABEL_35;
      }
    }
  }
  else
  {
    if ( a2 > 1937007731 )
    {
      if ( a2 == 1937007732 )
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
        LODWORD(v25) = ((*(_WORD *)(a1 + 32) & 0x1FF) << 8)
                     | (*(unsigned __int16 *)(a1 + 32) >> 9)
                     | (*(unsigned __int16 *)(a1 + 34) << 17);
        v20 = &qword_141B5C8A0;
        v24 = &qword_141B5C8A0;
        if ( &v24 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v21 = v24;
          v22 = v25;
          a3[1] = v25;
          *a3 = v21;
          v20 = (__int64 *)(sub_14083D4F0(v22) + 8);
          v25 = nullptr;
          v24 = v20;
        }
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v20 + 16))(v20, &v24);
        goto LABEL_42;
      }
      if ( a2 == 1954115685 )
      {
        v5 = *(char *)(a1 + 52);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v25) = v5;
        v24 = (__int64 *)v6;
        if ( &v24 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v12 = v24;
          v13 = v25;
          a3[1] = v25;
          *a3 = v12;
          v6 = sub_14083D4F0(v13) + 8;
          v25 = nullptr;
          v24 = (__int64 *)v6;
        }
        goto LABEL_35;
      }
      return v5;
    }
    if ( a2 == 1835103331 )
    {
      v5 = *(unsigned __int8 *)(a1 + 53);
      if ( (char)v5 > 0 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v25) = v5;
        v24 = (__int64 *)v6;
        if ( &v24 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v14 = v24;
          v15 = v25;
          a3[1] = v25;
          *a3 = v14;
          v6 = sub_14083D4F0(v15) + 8;
          v25 = nullptr;
          v24 = (__int64 *)v6;
        }
        goto LABEL_35;
      }
    }
    else
    {
      if ( a2 != 1851880553 )
        return v5;
      v5 = *(_DWORD *)(a1 + 44);
      if ( v5 != -1 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v25) = v5;
        v24 = (__int64 *)v6;
        if ( &v24 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v7 = v24;
          v8 = v25;
          a3[1] = v25;
          *a3 = v7;
          v6 = sub_14083D4F0(v8) + 8;
          v25 = nullptr;
          v24 = (__int64 *)v6;
        }
LABEL_35:
        (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v24);
LABEL_42:
        LOBYTE(v5) = 1;
        return v5;
      }
    }
  }
  LOBYTE(v5) = 1;
  if ( a3 != (__int64 **)&qword_141B5A4A0 )
  {
LABEL_37:
    (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
      qword_141B5A4A0,
      &qword_141B5A4A0,
      a3);
  }
  return v5;
}
