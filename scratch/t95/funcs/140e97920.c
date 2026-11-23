char __fastcall sub_140E97920(__int64 a1, int a2, __int64 *a3)
{
  __int64 v6; // rax
  __int64 v7; // rcx
  char result; // al
  int v9; // edi
  __int64 v10; // rax
  __int64 *v11; // rax
  __int64 v12; // rcx
  int v13; // edi
  __int64 *v14; // rax
  __int64 v15; // rcx
  int v16; // edi
  __int64 *v17; // rax
  __int64 v18; // rcx
  int v19; // edi
  __int64 *v20; // rax
  __int64 v21; // rcx
  int v22; // edi
  __int64 *v23; // rcx
  __int64 *v24; // rax
  __int64 v25; // rcx
  int v26; // edi
  __int64 *v27; // rax
  __int64 v28; // rcx
  int v29; // edi
  __int64 *v30; // rax
  __int64 v31; // rcx
  __int64 *v32; // [rsp+20h] [rbp-10h] BYREF
  __int64 v33; // [rsp+28h] [rbp-8h]
  __int64 v34; // [rsp+30h] [rbp+0h]

  v34 = -2;
  if ( a3 != &qword_141B5A4A0 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
      qword_141B5A4A0,
      &qword_141B5A4A0,
      a3);
  }
  v6 = *(_QWORD *)(a1 + 256);
  if ( v6 == 0 )
    return 0;
  v7 = *(_QWORD *)(v6 + 120);
  result = 1;
  if ( v7 != 0 )
  {
    result = 0;
    if ( a2 <= 1130720631 )
    {
      switch ( a2 )
      {
        case 1130717796:
          v22 = *(_DWORD *)(v7 + 8);
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
          LODWORD(v33) = (v22 << 8) & 0x1FF00 | (((unsigned __int16)v22 >> 9) + 2 * (v22 & 0xFFFF0000));
          v23 = &qword_141B5C8A0;
          v32 = &qword_141B5C8A0;
          if ( &v32 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v24 = v32;
            v25 = v33;
            a3[1] = v33;
            *a3 = (__int64)v24;
            v23 = (__int64 *)(sub_14083D4F0(v25) + 8);
            v33 = 0;
            v32 = v23;
          }
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v23 + 16))(v23, &v32);
          return 1;
        case 1130718068:
          v26 = *(char *)(v7 + 20);
          v10 = sub_14083D4F0(v7) + 40;
          LODWORD(v33) = v26;
          v32 = (__int64 *)v10;
          if ( &v32 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v27 = v32;
            v28 = v33;
            a3[1] = v33;
            *a3 = (__int64)v27;
            v10 = sub_14083D4F0(v28) + 8;
            v33 = 0;
            v32 = (__int64 *)v10;
          }
          break;
        case 1130720622:
          v13 = *(char *)(v7 + 21);
          v10 = sub_14083D4F0(v7) + 40;
          LODWORD(v33) = v13;
          v32 = (__int64 *)v10;
          if ( &v32 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v14 = v32;
            v15 = v33;
            a3[1] = v33;
            *a3 = (__int64)v14;
            v10 = sub_14083D4F0(v15) + 8;
            v33 = 0;
            v32 = (__int64 *)v10;
          }
          break;
        default:
          return result;
      }
    }
    else if ( a2 > 1130722411 )
    {
      if ( a2 == 1130722412 )
      {
        v29 = *(char *)(v7 + 18);
        v10 = sub_14083D4F0(v7) + 40;
        LODWORD(v33) = v29;
        v32 = (__int64 *)v10;
        if ( &v32 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v30 = v32;
          v31 = v33;
          a3[1] = v33;
          *a3 = (__int64)v30;
          v10 = sub_14083D4F0(v31) + 8;
          v33 = 0;
          v32 = (__int64 *)v10;
        }
      }
      else
      {
        if ( a2 != 1131246701 )
          return result;
        v16 = *(char *)(v7 + 19);
        v10 = sub_14083D4F0(v7) + 40;
        LODWORD(v33) = v16;
        v32 = (__int64 *)v10;
        if ( &v32 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v17 = v32;
          v18 = v33;
          a3[1] = v33;
          *a3 = (__int64)v17;
          v10 = sub_14083D4F0(v18) + 8;
          v33 = 0;
          v32 = (__int64 *)v10;
        }
      }
    }
    else if ( a2 == 1130720632 )
    {
      v19 = *(char *)(v7 + 22);
      v10 = sub_14083D4F0(v7) + 40;
      LODWORD(v33) = v19;
      v32 = (__int64 *)v10;
      if ( &v32 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v20 = v32;
        v21 = v33;
        a3[1] = v33;
        *a3 = (__int64)v20;
        v10 = sub_14083D4F0(v21) + 8;
        v33 = 0;
        v32 = (__int64 *)v10;
      }
    }
    else
    {
      if ( a2 != 1130721394 )
        return result;
      v9 = *(__int16 *)(v7 + 16);
      v10 = sub_14083D4F0(v7) + 40;
      LODWORD(v33) = v9;
      v32 = (__int64 *)v10;
      if ( &v32 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v11 = v32;
        v12 = v33;
        a3[1] = v33;
        *a3 = (__int64)v11;
        v10 = sub_14083D4F0(v12) + 8;
        v33 = 0;
        v32 = (__int64 *)v10;
      }
    }
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v10 + 16LL))(v10, &v32);
    return 1;
  }
  return result;
}
